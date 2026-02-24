"""
Global Input Manager - Win32 Low-Level Mouse Hook (Deadlock-Safe, 64-bit Clean)

Deux threads distincts :
  1. Hook thread (Python threading.Thread) — GetMessageW bloquant, jamais de sleep.
  2. QThread.run() — lit la queue, émet les signaux Qt en toute sécurité.

Toutes les fonctions Win32 ont leurs argtypes/restype définis explicitement
pour éviter les OverflowError sur les handles 64-bit (Windows x64).
"""

import ctypes
import ctypes.wintypes
import queue
import threading
import logging
import time

from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)

# ──────── Win32 constants ────────
WH_MOUSE_LL    = 14
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP   = 0x0205
WM_QUIT        = 0x0012

VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LSHIFT   = 0xA0
VK_RSHIFT   = 0xA1

# ──────── Typage explicite des fonctions Win32 (évite overflow 64-bit) ────────
_user32   = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32

# SetWindowsHookExW : retourne HHOOK (pointeur 64-bit) → c_void_p
_user32.SetWindowsHookExW.restype  = ctypes.c_void_p
_user32.SetWindowsHookExW.argtypes = [
    ctypes.c_int,     # idHook
    ctypes.c_void_p,  # lpfn (HOOKPROC)
    ctypes.c_void_p,  # hmod
    ctypes.c_uint32,  # dwThreadId
]

# CallNextHookEx : hhk = HHOOK (c_void_p), lParam = LPARAM (64-bit)
_user32.CallNextHookEx.restype  = ctypes.c_longlong
_user32.CallNextHookEx.argtypes = [
    ctypes.c_void_p,    # hhk
    ctypes.c_int,       # nCode
    ctypes.c_ulong,     # wParam (WPARAM)
    ctypes.c_longlong,  # lParam (LPARAM — pointeur 64-bit sur Win64)
]

# UnhookWindowsHookEx
_user32.UnhookWindowsHookEx.restype  = ctypes.c_bool
_user32.UnhookWindowsHookEx.argtypes = [ctypes.c_void_p]

# PostThreadMessageW : idThread = DWORD (c_uint32)
_user32.PostThreadMessageW.restype  = ctypes.c_bool
_user32.PostThreadMessageW.argtypes = [
    ctypes.c_uint32,   # idThread
    ctypes.c_uint,     # Msg
    ctypes.c_ulong,    # wParam
    ctypes.c_longlong, # lParam
]

# GetAsyncKeyState
_user32.GetAsyncKeyState.restype  = ctypes.c_short
_user32.GetAsyncKeyState.argtypes = [ctypes.c_int]

# GetCurrentThreadId
_kernel32.GetCurrentThreadId.restype  = ctypes.c_uint32
_kernel32.GetCurrentThreadId.argtypes = []


# ──────── Inline helpers ────────────────────────────────────────────────────

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt",          ctypes.wintypes.POINT),
        ("mouseData",   ctypes.wintypes.DWORD),
        ("flags",       ctypes.wintypes.DWORD),
        ("time",        ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


HOOKPROC = ctypes.WINFUNCTYPE(
    ctypes.c_longlong,  # return (LRESULT)
    ctypes.c_int,       # nCode
    ctypes.c_ulong,     # wParam (WPARAM)
    ctypes.c_longlong,  # lParam (LPARAM)
)


def _is_ctrl_pressed() -> bool:
    return (
        bool(_user32.GetAsyncKeyState(VK_LCONTROL) & 0x8000) or
        bool(_user32.GetAsyncKeyState(VK_RCONTROL) & 0x8000)
    )


def _is_shift_pressed() -> bool:
    return (
        bool(_user32.GetAsyncKeyState(VK_LSHIFT) & 0x8000) or
        bool(_user32.GetAsyncKeyState(VK_RSHIFT) & 0x8000)
    )


# ──────── InputManager ────────────────────────────────────────────────────


class InputManager(QThread):
    """
    Gestionnaire de raccourcis global via hook Win32 WH_MOUSE_LL.

    Architecture (deadlock-safe, 64-bit clean) :
      • hook_thread (threading.Thread) : GetMessageW bloquant, callback pur Win32.
        Ne touche JAMAIS à Qt — écrit seulement dans une queue Python.
      • QThread.run() : queue.get(timeout) + sig_shortcut_triggered.emit().

    Le callback retourne en < 1µs. Aucun risque de gel souris.
    """

    sig_shortcut_triggered = Signal(str, int, int)
    sig_error   = Signal(str)
    sig_started = Signal()
    sig_stopped = Signal()

    def __init__(self):
        super().__init__()
        self._running       = False
        self._hook_tid      = None
        self._hook_thread   = None
        self._hook_proc_ref = None          # gardé en mémoire pour éviter GC
        self._event_queue: queue.Queue = queue.Queue(maxsize=64)
        self._last_x = 0
        self._last_y = 0

    # ── Public API ──────────────────────────────────────────────

    def stop(self):
        logger.info("InputManager: Stopping")
        self._running = False
        if self._hook_tid:
            _user32.PostThreadMessageW(self._hook_tid, WM_QUIT, 0, 0)

    def get_last_position(self) -> tuple[int, int]:
        return (self._last_x, self._last_y)

    def is_running(self) -> bool:
        return self._running

    # ── QThread entry point ─────────────────────────────────────

    def run(self):
        self._running = True

        # Démarrer le hook dans un thread Python dédié
        self._hook_thread = threading.Thread(
            target=self._hook_thread_func,
            daemon=True,
            name="InputHookThread"
        )
        self._hook_thread.start()

        # Petite attente pour que le hook soit installé
        time.sleep(0.25)
        self.sig_started.emit()
        logger.info("InputManager: Signal dispatch loop started")

        # Émettre les signaux Qt depuis ce thread (safe avec QueuedConnection)
        while self._running:
            try:
                action, x, y = self._event_queue.get(timeout=0.1)
                self._last_x, self._last_y = x, y
                logger.info(f"InputManager: TRIGGER '{action}' at ({x}, {y})")
                self.sig_shortcut_triggered.emit(action, x, y)
            except queue.Empty:
                continue

        # Attendre la fin du hook thread
        if self._hook_thread and self._hook_thread.is_alive():
            self._hook_thread.join(timeout=2.0)

        self._running = False
        self.sig_stopped.emit()
        logger.info("InputManager: Stopped")

    # ── Hook thread ─────────────────────────────────────────────

    def _hook_thread_func(self):
        """
        Thread dédié avec boucle GetMessageW bloquante.
        Le callback écrit dans la queue et retourne immédiatement.
        Aucun appel Qt ici.
        """
        self._hook_tid = _kernel32.GetCurrentThreadId()
        hook_handle = ctypes.c_void_p(None)

        def _hook_proc(nCode: int, wParam: int, lParam: int) -> int:
            """Callback Win32 — doit retourner le plus vite possible."""
            try:
                if nCode >= 0 and wParam in (WM_RBUTTONDOWN, WM_RBUTTONUP):
                    if _is_ctrl_pressed():
                        if wParam == WM_RBUTTONUP:
                            data = ctypes.cast(
                                lParam, ctypes.POINTER(MSLLHOOKSTRUCT)
                            ).contents
                            x, y = data.pt.x, data.pt.y
                            action = "summarize" if _is_shift_pressed() else "show_menu"
                            try:
                                self._event_queue.put_nowait((action, x, y))
                            except queue.Full:
                                pass
                        return 1  # Supprimer l'event natif
            except Exception:
                pass  # Le callback NE PEUT PAS lever d'exception
            return _user32.CallNextHookEx(hook_handle, nCode, wParam, lParam)

        self._hook_proc_ref = HOOKPROC(_hook_proc)
        raw_hook = _user32.SetWindowsHookExW(
            WH_MOUSE_LL, self._hook_proc_ref, None, 0
        )

        if not raw_hook:
            err = ctypes.GetLastError()
            msg = f"SetWindowsHookExW échoué (erreur {err}). Relancer en Administrateur."
            logger.error(f"InputManager: {msg}")
            self.sig_error.emit(msg)
            return

        hook_handle.value = raw_hook
        logger.info(f"InputManager: Hook WH_MOUSE_LL installé (handle={raw_hook:#x})")

        # Boucle GetMessageW bloquante — JAMAIS de sleep ici
        msg = ctypes.wintypes.MSG()
        while True:
            ret = _user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if ret == 0 or ret == -1:
                break
            _user32.TranslateMessage(ctypes.byref(msg))
            _user32.DispatchMessageW(ctypes.byref(msg))

        if hook_handle.value:
            _user32.UnhookWindowsHookEx(hook_handle)
            logger.info("InputManager: Hook désinstallé")

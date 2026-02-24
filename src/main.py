"""
Main Application Entry Point

Orchestrates all components:
  - QApplication setup
  - Configuration loading
  - Health checks
  - Component initialization
  - Signal/slot connections
  - Main event loop

Usage:
    python -m src.main

    # Or directly:
    from src.main import QuickShortcutApp
    app = QuickShortcutApp()
    sys.exit(app.run())
"""

import sys
import logging
import time
import signal
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QThread, Signal, QObject

# Import core components
from src.core.config_service import ConfigService
from src.core.input_manager import InputManager
from src.core.shortcut_manager import ShortcutManager
from src.core.llm_provider import LLMProviderFactory
from src.services.health_check import HealthCheckManager

# Import UI components
from src.ui.floating_menu import FloatingMenu
from src.ui.response_window import ResponseWindow
from src.ui.inline_response import InlineResponseWindow
from src.ui.tray_icon import TrayIcon, TrayStatus
from src.ui.settings_dialog import SettingsDialog

# Import utilities
from src.core.clipboard_manager import get_clipboard_manager
import keyboard

logger = logging.getLogger(__name__)


class StreamingWorker(QObject):
    """Worker to run LLM streaming in a separate thread (non-blocking UI)"""

    # Signals
    token_received = Signal(str)  # Emit when token arrives
    streaming_complete = Signal()  # Emit when streaming finishes
    error_occurred = Signal(str)  # Emit when error happens

    def __init__(self, provider, messages, model):
        """Initialize worker with provider and messages"""
        super().__init__()
        self.provider = provider
        self.messages = messages
        self.model = model
        self._is_stopped = False

    def stop(self):
        """Request worker to stop processing"""
        self._is_stopped = True

    def run(self):
        """Run streaming in worker thread"""
        try:
            logger.info("Starting streaming in worker thread")
            token_count = 0

            for token in self.provider.stream_chat(self.messages, model=self.model):
                if getattr(self, '_is_stopped', False):
                    logger.info("Worker: Stream stopped by user")
                    break
                self.token_received.emit(token)
                token_count += 1

            logger.info(f"Streaming complete: {token_count} tokens")
            self.streaming_complete.emit()

        except Exception as e:
            if not getattr(self, '_is_stopped', False):
                logger.error(f"Streaming error in worker: {e}", exc_info=True)
                self.error_occurred.emit(str(e))


class QuickShortcutApp:
    """
    Main application class orchestrating all components.

    Initialization sequence:
    1. Load configuration
    2. Run health checks
    3. Initialize components
    4. Connect signals/slots
    5. Show UI (tray + input hooks)
    """

    def __init__(self):
        """Initialize application components"""
        logger.info("Initializing QuickShortcutApp")

        # Qt Application
        self.qapp = QApplication.instance() or QApplication(sys.argv)
        self.qapp.setApplicationName("Quick Shortcut AI")
        self.qapp.setApplicationVersion("0.1.0")
        self.qapp.setQuitOnLastWindowClosed(False)  # Ensure app doesn't close when settings dialog closes

        # Core components
        self.config = ConfigService()
        self.health_check = HealthCheckManager()
        self.shortcut_mgr = ShortcutManager()

        # UI components
        self.input_mgr = None
        self.floating_menu = None
        self.response_window = None
        self.inline_response = None
        self.tray_icon = None
        self.settings_dialog = None

        # State
        self._initialized = False
        self._running = False
        self._health_checks_passed = False

    def startup(self) -> bool:
        """
        Run startup sequence.

        Returns:
            bool: True if startup successful, False if failed
        """
        logger.info("Starting application")

        try:
            # 1. Load configuration
            self._load_config()

            # 2. Run health checks
            self._health_checks_passed = self._run_health_checks()
            if not self._health_checks_passed:
                logger.warning("Health checks failed, will show error status in tray icon")

            # 3. Initialize components
            self._init_components()

            # 4. Connect signals
            self._connect_signals()

            # 5. Show UI
            self._show_ui()

            self._initialized = True
            logger.info("Application startup complete")
            return True

        except Exception as e:
            logger.error(f"Startup failed: {e}", exc_info=True)
            QMessageBox.critical(
                None,
                "Startup Error",
                f"Failed to start application:\n{str(e)}\n\nCheck logs for details."
            )
            return False

    def _load_config(self):
        """Load configuration from file"""
        logger.info("Loading configuration")
        self.config.load()
        logger.info(f"Config loaded: {len(self.config.get_providers())} providers")

    def _run_health_checks(self) -> bool:
        """
        Run health checks at startup.

        Returns:
            bool: True if all checks passed
        """
        logger.info("Running health checks")

        all_passed, results = self.health_check.run_all_checks()

        # Log results
        for result in results:
            status = "[OK]" if result.passed else "[ERR]"
            logger.info(f"{status} {result.name}: {result.message}")

        if all_passed:
            logger.info("All health checks passed")
            # Icon will be set to READY later in run()
        else:
            logger.warning("Some health checks failed - health status will be shown in tray icon")
            # Will set tray icon to ERROR status in run() if checks failed

        return all_passed

    def _init_components(self):
        """Initialize all UI and core components"""
        logger.info("Initializing components")

        # Input hooks
        self.input_mgr = InputManager()
        logger.info("InputManager created")

        # Floating menu
        self.floating_menu = FloatingMenu()
        self._setup_menu_actions()
        logger.info("FloatingMenu created with actions")

        # Response window
        self.response_window = ResponseWindow()
        logger.info("ResponseWindow created")
        self.inline_response = InlineResponseWindow()
        logger.info("InlineResponseWindow created")

        # Tray icon
        self.tray_icon = TrayIcon()
        self._setup_tray_actions()
        logger.info("TrayIcon created with actions")

        # Settings dialog
        self.settings_dialog = SettingsDialog()
        logger.info("SettingsDialog created")

    def _setup_menu_actions(self):
        """Setup floating menu actions"""
        actions = [
            ("summarize", "Summarize"),
            ("translate", "Translate"),
            ("explain", "Explain"),
            ("code", "Generate Code"),
            ("screenshot", "Take Screenshot"),
        ]

        for action_id, label in actions:
            self.floating_menu.add_action(action_id, label)

        logger.info(f"Menu setup: {len(actions)} actions")

    def _setup_tray_actions(self):
        """Setup tray icon actions"""
        self.tray_icon.add_action("open_chat", "Open Chat")
        self.tray_icon.add_action("screenshot", "Take Screenshot")
        self.tray_icon.add_separator()
        self.tray_icon.add_action("settings", "Settings")
        self.tray_icon.add_separator()
        self.tray_icon.add_action("quit", "Quit")

        logger.info("Tray icon setup complete")

    def _connect_signals(self):
        """Connect all signal/slot connections"""
        logger.info("Connecting signals")

        # Input hooks -> Floating menu
        # Force QueuedConnection because the signal comes from a background thread
        # and we must modify GUI elements (like showing windows) in the main thread only.
        self.input_mgr.sig_shortcut_triggered.connect(
            self._on_shortcut_triggered,
            Qt.QueuedConnection
        )

        # Floating menu -> Response window
        self.floating_menu.sig_action_selected.connect(
            self._on_menu_action_selected
        )

        # Response window chat input -> LLM response
        self.response_window.sig_input_submitted.connect(
            self._on_chat_message_submitted
        )

        # Tray icon actions
        self.tray_icon.sig_action_triggered.connect(
            self._on_tray_action_triggered
        )

        # Input manager state
        self.input_mgr.sig_started.connect(
            lambda: logger.info("Input hooks started")
        )
        self.input_mgr.sig_stopped.connect(
            lambda: logger.info("Input hooks stopped")
        )

        # Response window signals
        self.response_window.sig_stop_requested.connect(
            self._on_stop_streaming
        )
        self.inline_response.sig_closed.connect(
            self._on_stop_streaming
        )

        # Settings dialog signals
        self.settings_dialog.sig_settings_changed.connect(
            self._on_settings_changed
        )

        logger.info("Signal connections complete")

    def _show_ui(self):
        """Show UI components"""
        logger.info("Showing UI")

        # Start input hooks
        self.input_mgr.start()

        # Show tray icon with appropriate status
        if self._health_checks_passed:
            logger.info("Health checks passed - showing READY status")
            self.tray_icon.set_status(TrayStatus.READY)
        else:
            logger.warning("Health checks failed - showing ERROR status")
            self.tray_icon.set_status(TrayStatus.ERROR)

        self.tray_icon.show()

        logger.info("UI shown and ready")

    def _on_shortcut_triggered(self, action_id: str, x: int, y: int):
        """Handle global shortcut trigger (Ctrl+Right-Click or Ctrl+Shift+Right-Click)"""
        logger.info(f"Main: Shortcut signal received: {action_id} at ({x}, {y})")

        # Capture active window BEFORE showing any UI
        # (once the menu or dialog appears, focus shifts away from the user's window)
        import ctypes
        self._pre_menu_window = ctypes.windll.user32.GetForegroundWindow()
        logger.info(f"Main: Saved active window handle: {self._pre_menu_window}")

        if action_id == "summarize":
            # Direct summarize with INLINE window (UX Modern)
            logger.info("Main: Executing direct summarize (Inline UX)")
            self.tray_icon.set_status(TrayStatus.BUSY)
            
            # Execute action targeting inline window (window will be shown AFTER clipboard capture to preserve focus)
            self._execute_action_inline("summarize")
        else:
            # Show floating menu (Premium look restored)
            logger.info("Main: Showing floating menu")
            self.tray_icon.set_status(TrayStatus.READY)
            self.floating_menu.show_at_cursor()

    def _execute_action_inline(self, action_id: str):
        """Execute an action using the Inline Response Window"""
        import ctypes
        logger.info(f"Main: [Auto-Copy] Starting for action '{action_id}'")
        
        # 0. Clear clipboard to ensure we only process new selection
        clipboard = QApplication.clipboard()
        clipboard.clear()
        
        # 1. Restore focus to the original application window before capturing
        # (the menu or app window may have stolen focus from e.g. Chrome)
        pre_menu_window = getattr(self, '_pre_menu_window', None)
        if pre_menu_window:
            logger.info(f"Main: [Auto-Copy] Restoring focus to window {pre_menu_window}")
            ctypes.windll.user32.SetForegroundWindow(pre_menu_window)
            time.sleep(0.15)  # Give OS time to actually shift focus
        
        # 2. Release modifiers first to avoid Ctrl+Shift+C or interference
        logger.info("Main: [Auto-Copy] Releasing physical modifiers (Shift, Ctrl)")
        keyboard.release('shift')
        keyboard.release('ctrl')
        time.sleep(0.05)
        
        # 3. Protect against SIGINT if the console is the active window (Ctrl+C kills Python)
        try:
            logger.info("Main: [Auto-Copy] Applying SIGINT protection")
            old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        except ValueError:
            old_handler = None # Not in main thread, ignore
            
        logger.info("Main: [Auto-Copy] Simulating Ctrl+C press...")
        keyboard.send('ctrl+c')
            
        time.sleep(0.1)
        if old_handler is not None:
            signal.signal(signal.SIGINT, old_handler)
            
        # 2. Wait for clipboard sync
        time.sleep(0.3)
        
        # 3. Capture clipboard content
        text = ""
        logger.info("Main: [Auto-Copy] Reading clipboard...")
        for i in range(3):
            text = clipboard.text().strip()
            if text:
                logger.info(f"Main: [Auto-Copy] Successfully captured {len(text)} characters from clipboard")
                break
            logger.info(f"Main: [Auto-Copy] Clipboard retry {i+1}/3")
            time.sleep(0.2)

        if not text:
            logger.warning("Clipboard capture failed: No text selected or clipboard empty")
            self.inline_response.clear()
            self.inline_response.show_at_cursor()
            self.inline_response.set_text("! Aucune sélection trouvée.\n\nVeuillez sélectionner du texte avant d'utiliser le raccourci.")
            self.tray_icon.set_status(TrayStatus.READY)
            return

        # Start streaming to inline window
        self.inline_response.clear()
        self.inline_response.show_at_cursor()
        self._stream_to_inline(action_id, text)

    def _on_menu_action_selected(self, action_id: str):
        """Handle floating menu action selection"""
        logger.info(f"Main: Menu action selected: {action_id}")
        
        try:
            # Actions like 'Settings' or 'Exit' don't use the inline window
            if action_id == "settings":
                self.settings_dialog.show()
                self.settings_dialog.raise_()
                self.settings_dialog.activateWindow()
                return
            elif action_id == "exit":
                self.exit_app()
                return

            # For AI actions, use the modern inline window as requested
            logger.info(f"Main: Launching inline execution for '{action_id}'")
            self.tray_icon.set_status(TrayStatus.BUSY)
            
            # Execute action targeting inline window (window will be shown AFTER clipboard capture to preserve focus)
            self._execute_action_inline(action_id)
            
        except Exception as e:
            logger.error(f"Main: ERROR in menu action selection: {e}", exc_info=True)
            self.tray_icon.set_status(TrayStatus.READY)
            # Try to show error in the inline window if possible
            if self.inline_response:
                self.inline_response.set_text(f"[ERR] Error: {str(e)}")
                self.inline_response.show_at_cursor()

    def _on_chat_message_submitted(self, user_message: str):
        """Handle user message submitted from chat input"""
        logger.info(f"Chat message received: {user_message[:50]}...")

        self.tray_icon.set_status(TrayStatus.BUSY)
        self._stream_chat_response(user_message)

    def _stream_to_inline(self, action_id: str, context_text: str):
        """Streaming logic specifically for the inline window"""
        logger.info(f"Main: Streaming '{action_id}' to inline window")
        
        # Assuming self.llm_manager exists and has get_current_provider()
        # If not, this part needs to be adapted to how providers are managed in the original code.
        # Based on _stream_chat_response and _stream_real_response, provider config is fetched directly.
        # Let's adapt this to match the existing pattern.
        
        provider_config = self.config.get_default_provider()
        if not provider_config:
            self.inline_response.set_text("❌ No AI Provider configured.\nPlease check Settings.")
            self.tray_icon.set_status(TrayStatus.READY)
            return

        try:
            provider_type = provider_config.get("type", "ollama")
            provider_init_config = {
                "base_url": provider_config.get("base_url", "http://localhost:11434"),
                "api_key": provider_config.get("api_key", ""),
            }
            provider = LLMProviderFactory.create(
                provider_type=provider_type,
                config=provider_init_config
            )
        except Exception as e:
            logger.error(f"Failed to create provider for inline stream: {e}")
            self.inline_response.set_text(f"❌ Failed to create provider: {str(e)}")
            self.tray_icon.set_status(TrayStatus.READY)
            return

        try:
            # 3. Get system/action prompt
            prompts = {
                "summarize": "Fais un résumé concis du texte suivant. Réponds impérativement dans la même langue que le texte source (ex: si le texte est en français, réponds en français) :",
                "translate": "Traduis le texte suivant en français :",
                "explain": "Explique le code ou le texte suivant en détail. Réponds impérativement dans la même langue que le texte source (ou en français si c'est du code) :",
                "code": "Génère du code pour accomplir la tâche suivante. Réponds impérativement dans la même langue que le texte source :",
                "screenshot": "Analyse la capture d'écran suivante et décris ce que tu vois. Réponds en français :",
            }
            system_prompt = prompts.get(action_id, "Please process the following text:")
            messages = [{"role": "user", "content": f"{system_prompt}\n\n{context_text}"}]

            # 4. Get model
            default_model = self.config.get("default_model")
            if default_model:
                model = default_model
            else:
                available_models = provider.get_available_models()
                model = available_models[0] if available_models else "llama2"

            # 5. Start threaded worker
            # Cleanup previous thread
            self._cleanup_thread('_inline_thread', '_inline_worker')

            self._inline_thread = QThread()
            self._inline_worker = StreamingWorker(provider, messages, model)
            self._inline_worker.moveToThread(self._inline_thread)

            # Signal connections
            self._inline_thread.started.connect(self._inline_worker.run)
            self._inline_worker.token_received.connect(self.inline_response.append_token)
            self._inline_worker.streaming_complete.connect(self._inline_thread.quit)
            self._inline_worker.streaming_complete.connect(self.inline_response.finish_streaming)
            self._inline_worker.error_occurred.connect(self._inline_thread.quit)
            self._inline_worker.error_occurred.connect(lambda e: self.inline_response.append_token(f"\n\n[ERR] Error: {e}"))
            
            # Final cleanup
            self._inline_thread.finished.connect(self._inline_worker.deleteLater)
            self._inline_thread.finished.connect(self._inline_thread.deleteLater)
            self._inline_thread.finished.connect(self._on_inline_finished)

            self._inline_thread.start()
            logger.info(f"Main: Inline streaming thread started for '{action_id}'")

        except Exception as e:
            logger.error(f"Failed to setup inline stream: {e}", exc_info=True)
            self.inline_response.append_token(f"\n\n❌ Configuration error: {str(e)}")
            self.tray_icon.set_status(TrayStatus.READY)


    def _on_inline_finished(self):
        """Cleanup after inline streaming finishes"""
        self.tray_icon.set_status(TrayStatus.READY)
        self._inline_thread = None
        logger.info("Main: Inline thread cleanup complete")

    def _stream_chat_response(self, user_message: str):
        """Stream LLM response for a chat message (non-blocking via QThread)"""
        try:
            # Get active provider config
            provider_config = self.config.get_default_provider()
            if not provider_config:
                logger.error("No provider configured")
                self.response_window.append_token("❌ No LLM provider configured. Please set one in Settings.")
                self.response_window.finish_streaming()
                self.tray_icon.set_status(TrayStatus.READY)
                return

            # Create provider instance from config
            provider_type = provider_config.get("type", "ollama")
            try:
                provider_init_config = {
                    "base_url": provider_config.get("base_url", "http://localhost:11434"),
                    "api_key": provider_config.get("api_key", ""),
                }
                provider = LLMProviderFactory.create(
                    provider_type=provider_type,
                    config=provider_init_config
                )
            except Exception as e:
                logger.error(f"Failed to create provider: {e}")
                self.response_window.append_token(f"❌ Failed to create provider: {str(e)}")
                self.response_window.finish_streaming()
                self.tray_icon.set_status(TrayStatus.READY)
                return

            logger.info(f"Chat with {provider.__class__.__name__}")

            # Build message format
            messages = [
                {"role": "user", "content": user_message}
            ]

            # Get model
            try:
                default_model = self.config.get("default_model")
                if default_model:
                    model = default_model
                else:
                    available_models = provider.get_available_models()
                    model = available_models[0] if available_models else "llama2"
            except Exception as e:
                logger.warning(f"Could not fetch models, using default: {e}")
                model = "llama2"

            logger.info(f"Chat using model: {model}")

            # Cleanup previous chat thread if running
            self._cleanup_thread('_chat_thread', '_chat_worker')

            # Start threaded worker (non-blocking)
            self._chat_thread = QThread()
            self._chat_worker = StreamingWorker(provider, messages, model)
            self._chat_worker.moveToThread(self._chat_thread)

            # Signal connections
            self._chat_thread.started.connect(self._chat_worker.run)
            self._chat_worker.token_received.connect(self.response_window.append_token)
            self._chat_worker.streaming_complete.connect(self._chat_thread.quit)
            self._chat_worker.streaming_complete.connect(self.response_window.finish_streaming)
            self._chat_worker.error_occurred.connect(self._chat_thread.quit)
            self._chat_worker.error_occurred.connect(
                lambda e: self.response_window.append_token(f"\n\n⚠️ Error during streaming: {e}")
            )

            # Final cleanup
            self._chat_thread.finished.connect(self._chat_worker.deleteLater)
            self._chat_thread.finished.connect(self._chat_thread.deleteLater)
            self._chat_thread.finished.connect(self._on_chat_finished)

            self._chat_thread.start()
            logger.info("Main: Chat streaming thread started")

        except Exception as e:
            logger.error(f"Error in chat response: {e}", exc_info=True)
            self.response_window.append_token(f"❌ Error: {str(e)}")
            self.response_window.finish_streaming()
            self.tray_icon.set_status(TrayStatus.READY)

    def _stream_real_response(self, action_id: str):
        """Stream real LLM response from configured provider (non-blocking via QThread)"""
        try:
            # 1. Get clipboard content
            clipboard_mgr = get_clipboard_manager()
            content = clipboard_mgr.get_text()

            if not content:
                logger.warning("Clipboard empty, cannot process")
                self.response_window.append_token("❌ Clipboard is empty. Please copy some text first.")
                self.response_window.finish_streaming()
                self.tray_icon.set_status(TrayStatus.READY)
                return

            # 2. Get active provider config
            provider_config = self.config.get_default_provider()
            if not provider_config:
                logger.error("No provider configured")
                self.response_window.append_token("❌ No LLM provider configured. Please set one in Settings.")
                self.response_window.finish_streaming()
                self.tray_icon.set_status(TrayStatus.READY)
                return

            # Create provider instance from config
            provider_type = provider_config.get("type", "ollama")
            try:
                provider_init_config = {
                    "base_url": provider_config.get("base_url", "http://localhost:11434"),
                    "api_key": provider_config.get("api_key", ""),
                }
                provider = LLMProviderFactory.create(
                    provider_type=provider_type,
                    config=provider_init_config
                )
            except Exception as e:
                logger.error(f"Failed to create provider: {e}")
                self.response_window.append_token(f"❌ Failed to create provider: {str(e)}")
                self.response_window.finish_streaming()
                self.tray_icon.set_status(TrayStatus.READY)
                return

            logger.info(f"Streaming {action_id} via {provider.__class__.__name__}")

            # 3. Create messages list based on action
            prompts = {
                "summarize": "Fais un résumé concis du texte suivant. Réponds en français:",
                "translate": "Traduis le texte suivant en français:",
                "explain": "Explique le code ou le texte suivant en détail. Réponds en français:",
                "code": "Génère du code pour accomplir la tâche suivante. Réponds en français:",
                "screenshot": "Analyse la capture d'écran suivante et décris ce que tu vois. Réponds en français:",
            }

            system_prompt = prompts.get(action_id, "Please process the following text:")

            messages = [
                {"role": "user", "content": f"{system_prompt}\n\n{content}"}
            ]

            # 4. Get model
            try:
                available_models = provider.get_available_models()
                model = available_models[0] if available_models else "llama2"
            except Exception as e:
                logger.warning(f"Could not fetch models, using default: {e}")
                model = "llama2"

            logger.info(f"Using model: {model}")

            # 5. Cleanup previous response thread if running
            self._cleanup_thread('_response_thread', '_response_worker')

            # Start threaded worker (non-blocking)
            self._response_thread = QThread()
            self._response_worker = StreamingWorker(provider, messages, model)
            self._response_worker.moveToThread(self._response_thread)

            # Signal connections
            self._response_thread.started.connect(self._response_worker.run)
            self._response_worker.token_received.connect(self.response_window.append_token)
            self._response_worker.streaming_complete.connect(self._response_thread.quit)
            self._response_worker.streaming_complete.connect(self.response_window.finish_streaming)
            self._response_worker.error_occurred.connect(self._response_thread.quit)
            self._response_worker.error_occurred.connect(
                lambda e: self.response_window.append_token(f"\n\n⚠️ Error during streaming: {e}")
            )

            # Final cleanup
            self._response_thread.finished.connect(self._response_worker.deleteLater)
            self._response_thread.finished.connect(self._response_thread.deleteLater)
            self._response_thread.finished.connect(self._on_response_finished)

            self._response_thread.start()
            logger.info(f"Main: Response streaming thread started for '{action_id}'")

        except Exception as e:
            logger.error(f"Error streaming response: {e}", exc_info=True)
            self.response_window.append_token(f"❌ Error: {str(e)}")
            self.response_window.finish_streaming()
            self.tray_icon.set_status(TrayStatus.READY)

    def _cleanup_thread(self, thread_attr: str, worker_attr: str):
        """Generic thread cleanup helper to prevent QThread destruction warnings."""
        try:
            thread = getattr(self, thread_attr, None)
            if thread:
                try:
                    if thread.isRunning():
                        logger.info(f"Main: Stopping previous {thread_attr}")
                        worker = getattr(self, worker_attr, None)
                        if worker:
                            worker.stop()
                        thread.quit()
                        thread.wait(500)
                        if thread.isRunning():
                            if not hasattr(self, '_zombie_threads'):
                                self._zombie_threads = []
                            self._zombie_threads.append(thread)
                except (RuntimeError, AttributeError):
                    logger.debug(f"Main: Previous {thread_attr} was already dead")
        except Exception as e:
            logger.error(f"Error cleaning up {thread_attr}: {e}")
        finally:
            setattr(self, thread_attr, None)

    def _on_chat_finished(self):
        """Cleanup after chat streaming finishes"""
        self.tray_icon.set_status(TrayStatus.READY)
        self._chat_thread = None
        logger.info("Main: Chat thread cleanup complete")

    def _on_response_finished(self):
        """Cleanup after response streaming finishes"""
        self.tray_icon.set_status(TrayStatus.READY)
        self._response_thread = None
        logger.info("Main: Response thread cleanup complete")

    def _on_tray_action_triggered(self, action_id: str):
        """Handle tray icon menu action"""
        logger.info(f"Tray action: {action_id}")

        if action_id == "open_chat":
            self.response_window.show()

        elif action_id == "quit":
            logger.info("Quit requested")
            self.shutdown()
            self.qapp.quit()

        elif action_id == "settings":
            logger.info("Settings requested")
            self.settings_dialog.exec()

    def _on_stop_streaming(self):
        """Handle stop streaming request (manually closed or stopped)"""
        logger.info("Stop streaming requested - cleaning up threads")
        
        try:
            if hasattr(self, '_inline_thread') and self._inline_thread:
                if self._inline_thread.isRunning():
                    logger.info("Main: Force stopping inline thread")
                    if hasattr(self, '_inline_worker') and self._inline_worker:
                        self._inline_worker.stop()
                    self._inline_thread.quit()
                    self._inline_thread.wait(500)
                    if self._inline_thread.isRunning():
                        if not hasattr(self, '_zombie_threads'):
                            self._zombie_threads = []
                        self._zombie_threads.append(self._inline_thread)
        except Exception as e:
            logger.error(f"Error stopping inline thread: {e}")
            
        self.tray_icon.set_status(TrayStatus.READY)

    def _on_settings_changed(self):
        """Handle settings changed signal"""
        logger.info("Settings changed, reloading configuration")
        # Reload config from file
        self.config.load()
        logger.info("Configuration reloaded")

        # Re-run health checks and update tray icon
        logger.info("Re-running health checks after settings change")
        health_checks_passed = self._run_health_checks()

        # Update tray icon based on new health check results
        if health_checks_passed:
            logger.info("Health checks now PASS - updating icon to READY")
            self.tray_icon.set_status(TrayStatus.READY)
        else:
            logger.warning("Health checks still FAIL - keeping icon as ERROR")
            self.tray_icon.set_status(TrayStatus.ERROR)

    def shutdown(self):
        """Shutdown application gracefully"""
        logger.info("Shutting down application")

        try:
            if self.input_mgr and self.input_mgr.is_running():
                self.input_mgr.stop()
                self.input_mgr.wait(2000)

            if self.tray_icon:
                self.tray_icon.close()

            if self.response_window:
                if self.response_window.isVisible():
                    self.response_window.close()

            if self.floating_menu:
                if self.floating_menu.isVisible():
                    self.floating_menu.close()

            if self.settings_dialog:
                if self.settings_dialog.isVisible():
                    self.settings_dialog.close()

            logger.info("Shutdown complete")

        except Exception as e:
            logger.error(f"Error during shutdown: {e}", exc_info=True)

    def run(self) -> int:
        """
        Run the application.

        Returns:
            int: Exit code (0 = success, 1 = error)
        """
        # Startup
        if not self.startup():
            return 1

        self._running = True

        # Run event loop
        try:
            logger.info("Starting event loop")
            return self.qapp.exec()

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self.shutdown()
            return 0

        except Exception as e:
            logger.error(f"Unhandled exception: {e}", exc_info=True)
            self.shutdown()
            return 1


def main():
    """Main entry point"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("quick_shortcut_ai.log")
        ]
    )

    logger.info("=" * 60)
    logger.info("Quick Shortcut AI - Starting up")
    logger.info("=" * 60)

    # Create and run app
    app = QuickShortcutApp()
    exit_code = app.run()

    logger.info("=" * 60)
    logger.info(f"Quick Shortcut AI - Exit code: {exit_code}")
    logger.info("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

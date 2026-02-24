
import ctypes
import time

def test_keys():
    print("Testing native GetKeyState (Ctrl=0x11, Shift=0x10)")
    print("Press Ctrl or Shift and see if they switch to 'Pressed'...")
    try:
        for _ in range(50):
            ctrl = (ctypes.windll.user32.GetKeyState(0x11) & 0x8000) != 0
            shift = (ctypes.windll.user32.GetKeyState(0x10) & 0x8000) != 0
            print(f"\rCtrl: {'PRESSED' if ctrl else '  OFF  '} | Shift: {'PRESSED' if shift else '  OFF  '}", end="", flush=True)
            time.sleep(0.1)
        print("\nTest complete.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    test_keys()

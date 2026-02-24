
import sys
import logging
import time
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt, QTimer, QPoint
from src.ui.floating_menu import FloatingMenu
from src.ui.response_window import ResponseWindow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Diagnostic")

def run_diagnostic():
    app = QApplication(sys.argv)
    
    # Force visible
    logger.info("TEST: Starting visibility diagnostic (Standard Window mode)")
    
    menu = FloatingMenu()
    menu.add_action("test", "ITEM DE TEST")
    
    resp = ResponseWindow()
    resp.set_context("test", "Diagnostic")
    resp.append_token("Ceci est un test.")
    resp.finish_streaming()

    def step_1():
        logger.info("Step 1: Showing FloatingMenu at 200, 200")
        menu.move(200, 200)
        menu.show()
        menu.raise_()
        logger.info(f"Menu: visible={menu.isVisible()}, geom={menu.geometry()}")

    def step_2():
        logger.info("Step 2: Showing ResponseWindow at 400, 400")
        resp.move(400, 400)
        resp.show()
        resp.raise_()
        logger.info(f"Response: visible={resp.isVisible()}, geom={resp.geometry()}")

    QTimer.singleShot(1000, step_1)
    QTimer.singleShot(3000, step_2)
    QTimer.singleShot(10000, app.quit)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    run_diagnostic()

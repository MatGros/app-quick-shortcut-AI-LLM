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
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

# Import core components
from src.core.config_service import ConfigService
from src.core.input_manager import InputManager
from src.core.shortcut_manager import ShortcutManager
from src.services.health_check import HealthCheckManager

# Import UI components
from src.ui.floating_menu import FloatingMenu
from src.ui.response_window import ResponseWindow
from src.ui.tray_icon import TrayIcon, TrayStatus

logger = logging.getLogger(__name__)


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

        # Core components
        self.config = ConfigService()
        self.health_check = HealthCheckManager()
        self.shortcut_mgr = ShortcutManager()

        # UI components
        self.input_mgr = None
        self.floating_menu = None
        self.response_window = None
        self.tray_icon = None

        # State
        self._initialized = False
        self._running = False

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
            if not self._run_health_checks():
                logger.warning("Health checks failed, continuing anyway")

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
            status = "✓" if result.passed else "✗"
            logger.info(f"{status} {result.name}: {result.message}")

        if all_passed:
            logger.info("All health checks passed")
        else:
            logger.warning("Some health checks failed")

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

        # Tray icon
        self.tray_icon = TrayIcon()
        self._setup_tray_actions()
        logger.info("TrayIcon created with actions")

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
        self.input_mgr.sig_shortcut_triggered.connect(
            self._on_shortcut_triggered
        )

        # Floating menu -> Response window
        self.floating_menu.sig_action_selected.connect(
            self._on_menu_action_selected
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

        logger.info("Signal connections complete")

    def _show_ui(self):
        """Show UI components"""
        logger.info("Showing UI")

        # Start input hooks
        self.input_mgr.start()

        # Show tray icon
        self.tray_icon.set_status(TrayStatus.READY)
        self.tray_icon.show()

        logger.info("UI shown and ready")

    def _on_shortcut_triggered(self, action_id: str, x: int, y: int):
        """Handle global shortcut trigger (Ctrl+Right-Click)"""
        logger.debug(f"Shortcut triggered: {action_id} at ({x}, {y})")

        self.tray_icon.set_status(TrayStatus.READY)
        self.floating_menu.show_at_cursor()

    def _on_menu_action_selected(self, action_id: str):
        """Handle floating menu action selection"""
        logger.info(f"Menu action selected: {action_id}")

        self.tray_icon.set_status(TrayStatus.BUSY)

        # Show response window
        self.response_window.set_context(action_id, "Running...")
        self.response_window.clear_response()
        self.response_window.show()

        # Simulate response (in real app, would call LLM provider)
        self._simulate_response(action_id)

    def _simulate_response(self, action_id: str):
        """Simulate LLM response (placeholder)"""
        # In real implementation, this would:
        # 1. Get clipboard content
        # 2. Call LLM provider
        # 3. Stream response tokens

        sample_responses = {
            "summarize": "This text provides an overview of the main topic. Key points include efficiency, scalability, and modern design patterns. The conclusion highlights best practices for implementation.",
            "translate": "Texte traduit en français: Ce code illustre les meilleures pratiques pour construire une application moderne et performante.",
            "explain": "This code defines a class that manages the application state. It handles configuration, user interactions, and displays results. The architecture follows the Model-View-Controller pattern.",
            "code": "def process_data(items):\n    return [item.strip().upper() for item in items if item]",
            "screenshot": "Screenshot analysis: The image shows a user interface with several interactive elements...",
        }

        response = sample_responses.get(action_id, f"Response for {action_id}")

        # Simulate streaming
        for token in response.split():
            self.response_window.append_token(token + " ")

        self.response_window.finish_streaming()
        self.tray_icon.set_status(TrayStatus.READY)

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
            logger.info("Settings requested (not implemented)")
            # TODO: Open settings dialog

    def _on_stop_streaming(self):
        """Handle stop streaming request"""
        logger.info("Stop streaming requested")
        self.tray_icon.set_status(TrayStatus.READY)

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

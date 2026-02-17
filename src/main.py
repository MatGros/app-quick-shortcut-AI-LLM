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
from src.ui.tray_icon import TrayIcon, TrayStatus
from src.ui.settings_dialog import SettingsDialog

# Import utilities
from src.core.clipboard_manager import get_clipboard_manager

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

    def run(self):
        """Run streaming in worker thread"""
        try:
            logger.info("Starting streaming in worker thread")
            token_count = 0

            for token in self.provider.stream_chat(self.messages, model=self.model):
                self.token_received.emit(token)
                token_count += 1

            logger.info(f"Streaming complete: {token_count} tokens")
            self.streaming_complete.emit()

        except Exception as e:
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

        # Core components
        self.config = ConfigService()
        self.health_check = HealthCheckManager()
        self.shortcut_mgr = ShortcutManager()

        # UI components
        self.input_mgr = None
        self.floating_menu = None
        self.response_window = None
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
            status = "✓" if result.passed else "✗"
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
        self.input_mgr.sig_shortcut_triggered.connect(
            self._on_shortcut_triggered
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

        # Stream real LLM response
        self._stream_real_response(action_id)

    def _on_chat_message_submitted(self, user_message: str):
        """Handle user message submitted from chat input"""
        logger.info(f"Chat message received: {user_message[:50]}...")

        self.tray_icon.set_status(TrayStatus.BUSY)
        self._stream_chat_response(user_message)

    def _stream_chat_response(self, user_message: str):
        """Stream LLM response for a chat message"""
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
                # Filter config to only include provider-specific parameters
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

            # Get model (from config default or first available)
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

            # Stream response tokens (keep UI responsive)
            token_count = 0
            try:
                for token in provider.stream_chat(messages, model=model):
                    self.response_window.append_token(token)
                    token_count += 1
                    # Keep UI responsive by processing Qt events
                    QApplication.processEvents()

                logger.info(f"Chat streaming complete: {token_count} tokens")

            except Exception as stream_error:
                logger.error(f"Chat streaming error: {stream_error}", exc_info=True)
                self.response_window.append_token(
                    f"\n\n⚠️ Error during streaming: {str(stream_error)}"
                )

            self.response_window.finish_streaming()

        except Exception as e:
            logger.error(f"Error in chat response: {e}", exc_info=True)
            self.response_window.append_token(f"❌ Error: {str(e)}")
            self.response_window.finish_streaming()

        finally:
            self.tray_icon.set_status(TrayStatus.READY)

    def _stream_real_response(self, action_id: str):
        """Stream real LLM response from configured provider"""
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
                # Filter config to only include provider-specific parameters
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

            # Build message format: [{"role": "user", "content": "..."}]
            messages = [
                {"role": "user", "content": f"{system_prompt}\n\n{content}"}
            ]

            # 4. Get model (first available or configured default)
            try:
                available_models = provider.get_available_models()
                model = available_models[0] if available_models else "llama2"
            except Exception as e:
                logger.warning(f"Could not fetch models, using default: {e}")
                model = "llama2"  # Default fallback

            logger.info(f"Using model: {model}")

            # 5. Stream response tokens (keep UI responsive)
            token_count = 0
            try:
                for token in provider.stream_chat(messages, model=model):
                    self.response_window.append_token(token)
                    token_count += 1
                    # Keep UI responsive by processing Qt events
                    QApplication.processEvents()

                logger.info(f"Streaming complete: {token_count} tokens")

            except Exception as stream_error:
                logger.error(f"Streaming error: {stream_error}", exc_info=True)
                self.response_window.append_token(
                    f"\n\n⚠️ Error during streaming: {str(stream_error)}"
                )

            self.response_window.finish_streaming()

        except Exception as e:
            logger.error(f"Error streaming response: {e}", exc_info=True)
            self.response_window.append_token(f"❌ Error: {str(e)}")
            self.response_window.finish_streaming()

        finally:
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
            logger.info("Settings requested")
            self.settings_dialog.exec()

    def _on_stop_streaming(self):
        """Handle stop streaming request"""
        logger.info("Stop streaming requested")
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

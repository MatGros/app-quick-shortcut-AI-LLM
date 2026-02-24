"""
Settings Dialog - Configuration UI

A tabbed dialog for managing:
  - LLM Provider configuration
  - Keyboard shortcuts
  - Appearance (theme, font)
  - Application information
"""

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QComboBox, QPushButton, QListWidget,
    QListWidgetItem, QSpinBox, QMessageBox, QFormLayout,
    QCheckBox, QGroupBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QFont
import logging

from src.core.config_service import ConfigService
from src.core.llm_provider import LLMProviderFactory

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    """Settings dialog with provider, shortcuts, and appearance tabs."""

    sig_settings_changed = Signal()  # Emitted when settings are saved

    def __init__(self, parent=None):
        """Initialize settings dialog."""
        super().__init__(parent)
        self.config_service = ConfigService()
        self.llm_factory = LLMProviderFactory()

        self.setWindowTitle("Quick Shortcut AI - Settings")
        self.setGeometry(100, 100, 600, 500)
        self.setModal(True)

        self._create_ui()
        self._load_settings()

    def _create_ui(self):
        """Create UI components."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self._create_providers_tab(), "Providers")
        tabs.addTab(self._create_shortcuts_tab(), "Shortcuts")
        tabs.addTab(self._create_appearance_tab(), "Appearance")
        tabs.addTab(self._create_about_tab(), "About")

        layout.addWidget(tabs)

        # Button bar
        button_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")
        btn_apply = QPushButton("Apply")

        btn_ok.clicked.connect(self._on_ok)
        btn_cancel.clicked.connect(self.reject)
        btn_apply.clicked.connect(self._on_apply)

        button_layout.addStretch()
        button_layout.addWidget(btn_apply)
        button_layout.addWidget(btn_ok)
        button_layout.addWidget(btn_cancel)

        layout.addLayout(button_layout)

    def _create_providers_tab(self) -> QWidget:
        """Create providers configuration tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Provider list
        layout.addWidget(QLabel("Configured Providers:"))
        self.provider_list = QListWidget()
        self.provider_list.itemSelectionChanged.connect(self._on_provider_selected)
        layout.addWidget(self.provider_list)

        # Provider details
        details_group = QGroupBox("Provider Details")
        details_layout = QFormLayout()

        self.provider_name = QLineEdit()
        self.provider_type = QComboBox()
        self.provider_type.addItems(["ollama", "openai", "anthropic"])
        self.provider_url = QLineEdit()
        self.provider_url.setPlaceholderText("http://localhost:11434")
        self.provider_api_key = QLineEdit()
        self.provider_api_key.setPlaceholderText("Leave empty if not needed")
        self.provider_api_key.setEchoMode(QLineEdit.Password)
        self.provider_model = QComboBox()
        self.provider_model.setEditable(True)
        self.provider_model.setPlaceholderText("Select or type model name")
        self.provider_enabled = QCheckBox("Enabled")

        details_layout.addRow("Name:", self.provider_name)
        details_layout.addRow("Type:", self.provider_type)
        details_layout.addRow("Base URL:", self.provider_url)
        details_layout.addRow("API Key:", self.provider_api_key)
        details_layout.addRow("Default Model:", self.provider_model)
        details_layout.addRow("", self.provider_enabled)

        # Connect type change to refresh models
        self.provider_type.currentTextChanged.connect(self._on_provider_type_changed)
        self.provider_url.textChanged.connect(self._on_provider_url_changed)

        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        # Action buttons
        action_layout = QHBoxLayout()
        btn_test = QPushButton("Test Connection")
        btn_test.clicked.connect(self._on_test_connection)
        btn_refresh_models = QPushButton("Refresh Models")
        btn_refresh_models.clicked.connect(self._refresh_available_models)
        btn_save_provider = QPushButton("Save Provider")
        btn_save_provider.clicked.connect(self._on_save_provider)
        btn_delete = QPushButton("Delete Provider")
        btn_delete.clicked.connect(self._on_delete_provider)

        action_layout.addWidget(btn_test)
        action_layout.addWidget(btn_refresh_models)
        action_layout.addWidget(btn_save_provider)
        action_layout.addWidget(btn_delete)
        action_layout.addStretch()

        layout.addLayout(action_layout)

        widget.setLayout(layout)
        return widget

    def _create_shortcuts_tab(self) -> QWidget:
        """Create keyboard shortcuts tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Keyboard Shortcuts:"))

        # Shortcuts list
        self.shortcuts_list = QListWidget()
        shortcuts = self.config_service.get("shortcuts", {})
        for shortcut_name, shortcut_key in shortcuts.items():
            item = QListWidgetItem(f"{shortcut_name}: {shortcut_key}")
            item.setData(Qt.UserRole, shortcut_name)
            self.shortcuts_list.addItem(item)

        layout.addWidget(self.shortcuts_list)

        # Info
        layout.addWidget(QLabel(
            "Shortcut editing coming in future version.\n"
            "Currently shortcuts are configured in the config file."
        ))

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def _create_appearance_tab(self) -> QWidget:
        """Create appearance configuration tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Theme selection
        theme_group = QGroupBox("Theme")
        theme_layout = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light", "system"])
        theme_layout.addRow("Theme:", self.theme_combo)

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Font settings
        font_group = QGroupBox("Font")
        font_layout = QFormLayout()

        self.font_family = QLineEdit()
        self.font_size = QSpinBox()
        self.font_size.setMinimum(8)
        self.font_size.setMaximum(24)

        font_layout.addRow("Family:", self.font_family)
        font_layout.addRow("Size:", self.font_size)

        font_group.setLayout(font_layout)
        layout.addWidget(font_group)

        # Animation
        animation_group = QGroupBox("Animation")
        animation_layout = QFormLayout()

        self.animation_speed = QSpinBox()
        self.animation_speed.setMinimum(0)
        self.animation_speed.setMaximum(1000)
        self.animation_speed.setValue(200)
        self.animation_speed.setSuffix(" ms")

        animation_layout.addRow("Animation Speed:", self.animation_speed)

        animation_group.setLayout(animation_layout)
        layout.addWidget(animation_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def _create_about_tab(self) -> QWidget:
        """Create about tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        about_text = QLabel(
            "<h2>Quick Shortcut AI</h2>"
            "<p>A lightweight, ultra-fast Windows native application for "
            "AI-powered text assistance with global keyboard shortcuts.</p>"
            "<p><b>Version:</b> 1.0.0</p>"
            "<p><b>Framework:</b> Python 3.10+ with PySide6</p>"
            "<p><b>License:</b> GPL-3.0</p>"
            "<p><b>Supported Providers:</b> Ollama, OpenAI, Anthropic</p>"
        )
        about_text.setOpenExternalLinks(True)

        layout.addWidget(about_text)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def _load_settings(self):
        """Load current settings into UI."""
        # Load providers
        self._load_providers()

        # Load appearance
        theme = self.config_service.get("appearance.theme", "dark")
        self.theme_combo.setCurrentText(theme)

        font_family = self.config_service.get("appearance.font_family", "Segoe UI")
        self.font_family.setText(font_family)

        font_size = self.config_service.get("appearance.font_size", 11)
        self.font_size.setValue(font_size)

        animation_speed = self.config_service.get("appearance.animation_speed_ms", 200)
        self.animation_speed.setValue(animation_speed)

    def _load_providers(self):
        """Load providers into list and select default."""
        self.provider_list.clear()
        providers = self.config_service.get_providers()
        default_provider = self.config_service.get("default_provider")

        default_item = None
        for provider in providers:
            provider_id = provider.get("id", "unknown")
            provider_name = provider.get("name", provider_id)
            enabled = provider.get("enabled", False)

            # Bold text if default
            if provider_id == default_provider:
                item_text = f"* {provider_name}"
            else:
                item_text = provider_name

            if not enabled:
                item_text += " (disabled)"

            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, provider_id)
            self.provider_list.addItem(item)
            
            if provider_id == default_provider:
                default_item = item

        # Select default item if found
        if default_item:
            self.provider_list.setCurrentItem(default_item)
        elif self.provider_list.count() > 0:
            self.provider_list.setCurrentRow(0)

    def _on_provider_selected(self):
        """Load selected provider details."""
        if not self.provider_list.selectedItems():
            self.provider_name.clear()
            self.provider_url.clear()
            self.provider_api_key.clear()
            self.provider_model.clear()
            self.provider_enabled.setChecked(False)
            return

        item = self.provider_list.selectedItems()[0]
        provider_id = item.data(Qt.UserRole)

        providers = self.config_service.get_providers()
        for provider in providers:
            if provider.get("id") == provider_id:
                self.provider_name.setText(provider.get("name", ""))
                self.provider_type.setCurrentText(provider.get("type", "ollama"))
                self.provider_url.setText(provider.get("base_url", ""))
                self.provider_api_key.setText(provider.get("api_key", ""))
                default_model = provider.get("default_model", "")
                if default_model:
                    self.provider_model.setEditText(default_model)
                self.provider_enabled.setChecked(provider.get("enabled", False))
                break

    def _on_test_connection(self):
        """Test provider connection."""
        provider_type = self.provider_type.currentText()
        base_url = self.provider_url.text()
        api_key = self.provider_api_key.text()

        try:
            # Create temporary provider instance with correct config dict
            config = {
                "base_url": base_url,
                "api_key": api_key if api_key else "",
            }
            provider = self.llm_factory.create(
                provider_type=provider_type,
                config=config
            )

            # Test connection (health check)
            is_healthy = provider.health_check()

            if is_healthy:
                QMessageBox.information(
                    self,
                    "Connection Test",
                    "[OK] Connection successful!\n"
                    "Provider is responding correctly."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Connection Test",
                    "[ERR] Connection failed.\n"
                    "Provider did not respond successfully."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Connection Test",
                f"[ERR] Error testing connection:\n{str(e)}"
            )

    def _on_provider_type_changed(self):
        """Handle provider type change - refresh available models."""
        self._refresh_available_models()

    def _on_provider_url_changed(self):
        """Handle provider URL change - refresh available models."""
        self._refresh_available_models()

    def _refresh_available_models(self):
        """Fetch and display available models from the selected provider."""
        provider_type = self.provider_type.currentText()
        base_url = self.provider_url.text()
        api_key = self.provider_api_key.text()

        if not base_url:
            self.provider_model.clear()
            return

        try:
            # Create temporary provider instance
            config = {
                "base_url": base_url,
                "api_key": api_key if api_key else "",
            }
            provider = self.llm_factory.create(
                provider_type=provider_type,
                config=config
            )

            # Get available models if provider supports it
            if hasattr(provider, 'get_available_models'):
                try:
                    models = provider.get_available_models()
                    self.provider_model.clear()
                    for model in models:
                        self.provider_model.addItem(model)
                    if models:
                        self.provider_model.setCurrentIndex(0)
                except Exception as e:
                    logger.warning(f"Could not fetch models: {e}")
                    self.provider_model.clear()
            else:
                self.provider_model.clear()
        except Exception as e:
            logger.warning(f"Could not create provider for model listing: {e}")
            self.provider_model.clear()

    def _on_save_provider(self):
        """Save provider configuration."""
        if not self.provider_list.selectedItems():
            QMessageBox.warning(self, "Select Provider", "Please select a provider to save.")
            return

        item = self.provider_list.selectedItems()[0]
        provider_id = item.data(Qt.UserRole)

        # Collect updated values
        provider_config = {
            "id": provider_id,
            "name": self.provider_name.text(),
            "type": self.provider_type.currentText(),
            "base_url": self.provider_url.text(),
            "api_key": self.provider_api_key.text(),
            "default_model": self.provider_model.currentText(),
            "enabled": self.provider_enabled.isChecked(),
        }

        # Validate
        if not provider_config["name"]:
            QMessageBox.warning(self, "Validation", "Provider name cannot be empty.")
            return

        if not provider_config["base_url"]:
            QMessageBox.warning(self, "Validation", "Base URL cannot be empty.")
            return

        # Save
        self.config_service.add_provider(provider_id, provider_config)

        QMessageBox.information(self, "Success", "Provider configuration saved.")
        self._load_providers()

    def _on_delete_provider(self):
        """Delete selected provider."""
        if not self.provider_list.selectedItems():
            QMessageBox.warning(self, "Select Provider", "Please select a provider to delete.")
            return

        item = self.provider_list.selectedItems()[0]
        provider_id = item.data(Qt.UserRole)

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this provider?\n"
            f"This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            providers = self.config_service.get("providers", [])
            providers = [p for p in providers if p.get("id") != provider_id]
            self.config_service.set("providers", providers)

            QMessageBox.information(self, "Success", "Provider deleted.")
            self._load_providers()

    def _on_apply(self):
        """Apply settings without closing dialog."""
        self._save_settings()
        QMessageBox.information(self, "Applied", "Settings applied successfully.")

    def _on_ok(self):
        """Apply settings and close dialog."""
        self._save_settings()
        self.accept()

    def _save_settings(self):
        """Save all settings to config."""
        # Auto-save the currently selected provider details
        if self.provider_list.selectedItems():
            provider_id = self.provider_list.selectedItems()[0].data(Qt.UserRole)
            provider_config = {
                "id": provider_id,
                "name": self.provider_name.text(),
                "type": self.provider_type.currentText(),
                "base_url": self.provider_url.text() or self.provider_url.placeholderText() or "http://localhost:11434",
                "api_key": self.provider_api_key.text(),
                "default_model": self.provider_model.currentText(),
                "enabled": self.provider_enabled.isChecked() if self.provider_enabled.isChecked() else True, # default to True
            }
            self.config_service.add_provider(provider_id, provider_config)

        # Save appearance
        self.config_service.set("appearance.theme", self.theme_combo.currentText())
        self.config_service.set("appearance.font_family", self.font_family.text())
        self.config_service.set("appearance.font_size", self.font_size.value())
        self.config_service.set("appearance.animation_speed_ms", self.animation_speed.value())

        # Save config to file
        self.config_service.save()

        # Emit signal
        self.sig_settings_changed.emit()

        logger.info("Settings saved")

    def closeEvent(self, event):
        """Handle window close - hide instead of closing app"""
        logger.debug("SettingsDialog close requested - hiding dialog")
        # Don't call self.accept() here — it's already called by _on_ok().
        # Simply hide the dialog to prevent the app from exiting.
        self.hide()
        event.ignore()

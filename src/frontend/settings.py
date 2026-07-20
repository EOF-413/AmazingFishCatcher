import os
import sys
import winreg

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox,
    QMessageBox, QCheckBox
)

from src.config import load_config, save_config, DEFAULT_CONFIG, APP_FULL_NAME


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.config = load_config()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #ffffff;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
            QCheckBox {
                color: #ffffff;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #2a2a2a;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border: 1px solid #0078d4;
                border-radius: 3px;
            }
        """)

        capture_group = QGroupBox("Параметры захвата")
        capture_layout = QGridLayout()
        capture_layout.setSpacing(10)
        capture_layout.setHorizontalSpacing(15)

        label_hold = QLabel("Время удержания (сек):")
        label_hold.setStyleSheet("color: #ffffff;")
        capture_layout.addWidget(label_hold, 0, 0)

        self.hold_edit = QLineEdit(str(self.config["HOLD"]))
        self.hold_edit.setFixedWidth(80)
        capture_layout.addWidget(self.hold_edit, 0, 1)

        label_cooldown = QLabel("Задержка между кадрами (сек):")
        label_cooldown.setStyleSheet("color: #ffffff;")
        capture_layout.addWidget(label_cooldown, 1, 0)

        self.cooldown_edit = QLineEdit(str(self.config["COOLDOWN"]))
        self.cooldown_edit.setFixedWidth(80)
        capture_layout.addWidget(self.cooldown_edit, 1, 1)

        label_match = QLabel("Порог совпадения (0.1-0.9):")
        label_match.setStyleSheet("color: #ffffff;")
        capture_layout.addWidget(label_match, 2, 0)

        self.min_match_edit = QLineEdit(str(self.config["MIN_MATCH"]))
        self.min_match_edit.setFixedWidth(80)
        capture_layout.addWidget(self.min_match_edit, 2, 1)

        capture_group.setLayout(capture_layout)
        layout.addWidget(capture_group)

        window_group = QGroupBox("Настройки окна")
        window_layout = QVBoxLayout()
        window_layout.setSpacing(8)

        self.top_checkbox = QCheckBox("Поверх всех окон")
        self.top_checkbox.setChecked(self.config.get("ALWAYS_ON_TOP", True))
        self.top_checkbox.stateChanged.connect(self._on_checkbox_changed)
        window_layout.addWidget(self.top_checkbox)

        self.auto_start_checkbox = QCheckBox("Автозапуск с Windows")
        self.auto_start_checkbox.setChecked(self._is_autostart_enabled())
        self.auto_start_checkbox.stateChanged.connect(self._on_autostart_changed)
        window_layout.addWidget(self.auto_start_checkbox)

        self.tray_checkbox = QCheckBox("Сворачивать в трей при закрытии")
        self.tray_checkbox.setChecked(self.config.get("MINIMIZE_TO_TRAY", False))
        self.tray_checkbox.stateChanged.connect(self._on_checkbox_changed)
        window_layout.addWidget(self.tray_checkbox)

        window_group.setLayout(window_layout)
        layout.addWidget(window_group)

        reset_btn = QPushButton("Сбросить настройки")
        reset_btn.setFixedWidth(250)
        reset_btn.setFixedHeight(40)
        reset_btn.clicked.connect(self._reset_settings)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
        """)

        layout.addWidget(reset_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

    def _is_autostart_enabled(self):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, APP_FULL_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False

    def _set_autostart(self, enabled):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            if enabled:
                if getattr(sys, 'frozen', False):
                    exe_path = sys.executable
                else:
                    exe_path = sys.argv[0]
                winreg.SetValueEx(key, APP_FULL_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
                if self.parent_window:
                    self.parent_window.log("Автозапуск с Windows включен", 'info')
            else:
                try:
                    winreg.DeleteValue(key, APP_FULL_NAME)
                    if self.parent_window:
                        self.parent_window.log("Автозапуск с Windows отключен", 'info')
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            if self.parent_window:
                self.parent_window.log(f"Ошибка при настройке автозапуска: {e}", 'error')

    def _on_autostart_changed(self):
        enabled = self.auto_start_checkbox.isChecked()
        self._set_autostart(enabled)

    def _on_checkbox_changed(self):
        self.config["ALWAYS_ON_TOP"] = self.top_checkbox.isChecked()
        self.config["MINIMIZE_TO_TRAY"] = self.tray_checkbox.isChecked()
        
        save_config(self.config)
        
        if self.parent_window:
            self.parent_window.config = load_config()
            
            if self.config["ALWAYS_ON_TOP"]:
                self.parent_window.setWindowFlags(
                    self.parent_window.windowFlags() | Qt.WindowStaysOnTopHint
                )
            else:
                self.parent_window.setWindowFlags(
                    self.parent_window.windowFlags() & ~Qt.WindowStaysOnTopHint
                )
            self.parent_window.show()

    def _reset_settings(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Сбросить все настройки к значениям по умолчанию?")
        msg_box.setInformativeText("Это действие нельзя отменить.")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            QPushButton {
                color: #ffffff;
                background-color: #3d3d3d;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px 15px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #5d5d5d;
            }
        """)

        for button in msg_box.buttons():
            if msg_box.buttonRole(button) == QMessageBox.YesRole:
                button.setText("Да")
            elif msg_box.buttonRole(button) == QMessageBox.NoRole:
                button.setText("Нет")

        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            self.config.update(DEFAULT_CONFIG)
            save_config(self.config)

            self.hold_edit.setText(str(self.config["HOLD"]))
            self.cooldown_edit.setText(str(self.config["COOLDOWN"]))
            self.min_match_edit.setText(str(self.config["MIN_MATCH"]))
            self.top_checkbox.setChecked(self.config["ALWAYS_ON_TOP"])
            self.tray_checkbox.setChecked(self.config["MINIMIZE_TO_TRAY"])

            if self.parent_window:
                self.parent_window.config = load_config()
                self.parent_window.log("Настройки сброшены к значениям по умолчанию", 'settings')

    def get_values(self):
        try:
            return {
                "HOLD": float(self.hold_edit.text()),
                "COOLDOWN": float(self.cooldown_edit.text()),
                "MIN_MATCH": float(self.min_match_edit.text())
            }
        except ValueError:
            return None

    def save_settings(self):
        values = self.get_values()
        if values is None:
            return

        changed = False
        for key, val in values.items():
            if key in self.config and self.config[key] != val:
                if key == "HOLD" and 0.1 <= val <= 3.0:
                    self.config[key] = val
                    changed = True
                elif key == "COOLDOWN" and 0.1 <= val <= 2.0:
                    self.config[key] = val
                    changed = True
                elif key == "MIN_MATCH" and 0.1 <= val <= 0.9:
                    self.config[key] = val
                    changed = True

        if changed:
            save_config(self.config)
            if self.parent_window:
                self.parent_window.config = load_config()

    def update_config(self):
        self.save_settings()

    def set_enabled(self, enabled):
        self.hold_edit.setEnabled(enabled)
        self.cooldown_edit.setEnabled(enabled)
        self.min_match_edit.setEnabled(enabled)
        self.top_checkbox.setEnabled(enabled)
        self.auto_start_checkbox.setEnabled(enabled)
        self.tray_checkbox.setEnabled(enabled)

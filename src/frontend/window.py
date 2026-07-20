import os
import sys
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QTextCharFormat, QTextCursor, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QGroupBox, QTabWidget,
    QSystemTrayIcon, QMenu, QAction
)

from src.config import load_config, VER, APP_FULL_NAME
from src.frontend.settings import SettingsTab


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class ColoredTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: none;
                font-family: Consolas;
                font-size: 10pt;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.formats = {
            'info': self._create_format("#09ff00"),
            'warning': self._create_format('#ffaa00'),
            'error': self._create_format('#ff4444'),
            'default': self._create_format('#ffffff'),
            'settings': self._create_format("#7700ffff"),
            'keyboard': self._create_format("#8c45ff42"),
            'nokey': self._create_format("#ffce2e42"),
        }

    def _create_format(self, color):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        return fmt

    def append_colored(self, text, tag='default'):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        ts = datetime.now().strftime("%H:%M:%S")
        self.textCursor().insertText(f"[{ts}] ", self.formats['default'])
        self.textCursor().insertText(f"{text}\n", self.formats.get(tag, self.formats['default']))
        self.ensureCursorVisible()
        QApplication.processEvents()


class MainWindow(QMainWindow):
    append_text = pyqtSignal(str, str)

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.config = load_config()
        self.tray_icon = None
        self.tray_menu = None
        self._closing = False
        self._toggle_lock = False
        self._last_toggle_time = 0

        self.setWindowTitle(APP_FULL_NAME)
        self.resize(400, 600)
        self.setMinimumSize(400, 600)

        if self.config.get("ALWAYS_ON_TOP", True):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        icon_path = resource_path('icon.ico')
        if os.path.exists(icon_path):
            try:
                icon = QIcon(icon_path)
                self.setWindowIcon(icon)
                self._create_tray_icon(icon)
            except Exception:
                pass

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
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
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 10px 30px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #1a8ad4;
            }
            QPushButton:pressed {
                background-color: #0066b8;
            }
            QPushButton#stop_btn {
                background-color: #d32f2f;
            }
            QPushButton#stop_btn:hover {
                background-color: #e53935;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #ffffff;
                padding: 8px 20px;
                border: 1px solid #3d3d3d;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #3d3d3d;
            }
            QTabBar::tab:disabled {
                color: #666666;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(0, 0, 0, 10)

        title = QLabel(APP_FULL_NAME)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        header_layout.addWidget(title)

        version_label = QLabel(f"v{VER}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 15px; color: #888888;")
        header_layout.addWidget(version_label)

        layout.addWidget(header_widget)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_main_tab(), "Главная")
        self.settings_tab = SettingsTab(self)
        self.tabs.addTab(self.settings_tab, "Настройки")
        layout.addWidget(self.tabs)

        self.start_btn = QPushButton("СТАРТ")
        self.start_btn.clicked.connect(self._on_start_click)
        self.start_btn.setFixedWidth(180)
        self.start_btn.setFixedHeight(40)

        bottom_layout = QVBoxLayout()
        bottom_layout.setSpacing(8)
        bottom_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        layout.addLayout(bottom_layout)

        self.append_text.connect(self._append_text_slot)

        self.timer = QTimer()
        self.timer.timeout.connect(self._auto_save_settings)
        self.timer.start(2000)

        self.app.start_listener()
        self.app.gui = self

    def _auto_save_settings(self):
        if self.settings_tab:
            self.settings_tab.save_settings()

    def _create_tray_icon(self, icon):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)

        self.tray_menu = QMenu()

        show_action = QAction("Показать", self)
        show_action.triggered.connect(self.show)
        self.tray_menu.addAction(show_action)

        self.tray_menu.addSeparator()

        toggle_action = QAction("Старт/Стоп", self)
        toggle_action.triggered.connect(self._on_tray_toggle)
        self.tray_menu.addAction(toggle_action)

        self.tray_menu.addSeparator()

        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(self._quit_application)
        self.tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self._tray_icon_activated)
        self.tray_icon.show()

    def _tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()

    def _quit_application(self):
        if self._closing:
            return
        self._closing = True

        if self.settings_tab:
            self.settings_tab.save_settings()

        self.app.cleanup()
        if self.tray_icon:
            self.tray_icon.hide()
        QApplication.quit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F9 and not event.isAutoRepeat():
            self._on_toggle()
            event.accept()
            return
        super().keyPressEvent(event)

    def _on_start_click(self):
        self._on_toggle()

    def _on_tray_toggle(self):
        self._on_toggle()

    def _on_toggle(self):
        import time
        current_time = time.time()
        if self._toggle_lock or (current_time - self._last_toggle_time) < 0.5:
            return

        self._toggle_lock = True
        self._last_toggle_time = current_time

        try:
            self.app.toggle()
            self.update_status()
            self._update_fields_state()
        except Exception as e:
            self.log(f"Ошибка при переключении: {e}", 'error')
        finally:
            self._toggle_lock = False

    def _append_text_slot(self, text, tag):
        self.log_area.append_colored(text, tag)

    def _create_main_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        log_frame = QGroupBox("Лог")
        log_layout = QVBoxLayout()
        self.log_area = ColoredTextEdit()
        log_layout.addWidget(self.log_area)
        log_frame.setLayout(log_layout)
        layout.addWidget(log_frame)

        return tab

    def log(self, message, tag='default'):
        self.append_text.emit(message, tag)

    def log_info(self, message):
        self.log(message, 'info')

    def log_warning(self, message):
        self.log(message, 'warning')

    def log_error(self, message):
        self.log(message, 'error')

    def update_status(self):
        if self.app.enabled:
            self.start_btn.setText("СТОП")
            self.start_btn.setObjectName("stop_btn")
        else:
            self.start_btn.setText("СТАРТ")
            self.start_btn.setObjectName("")
        self.start_btn.style().unpolish(self.start_btn)
        self.start_btn.style().polish(self.start_btn)

    def _update_fields_state(self):
        enabled = not self.app.enabled
        self.settings_tab.set_enabled(enabled)
        self.tabs.setTabEnabled(1, enabled)

    def closeEvent(self, event):
        if self._closing:
            event.accept()
            return

        if self.settings_tab:
            self.settings_tab.save_settings()

        self.config = load_config()

        if self.config.get("MINIMIZE_TO_TRAY", False):
            if self.tray_icon and self.tray_icon.isVisible():
                self.hide()
                if self.tray_icon:
                    self.tray_icon.showMessage(
                        APP_FULL_NAME,
                        "Приложение свернуто в трей",
                        QSystemTrayIcon.Information,
                        2000
                    )
                event.ignore()
                return
            else:
                self.showMinimized()
                event.ignore()
                return

        self._closing = True
        try:
            self.app.cleanup()
            if self.tray_icon:
                self.tray_icon.hide()
        except Exception:
            pass
        event.accept()

    def showEvent(self, event):
        super().showEvent(event)

    def show(self):
        super().show()

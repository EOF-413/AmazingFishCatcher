import sys
import os
import traceback

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from src import App
from src.frontend import MainWindow


if __name__ == '__main__':
    try:

        QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)

        app = QApplication(sys.argv)

        auto_app = App()
        window = MainWindow(auto_app)
        auto_app.gui = window
        window.log_info("Нажмите F9 для старта/остановки")
        window.show()

        exit_code = app.exec_()
        auto_app.cleanup()
        sys.exit(exit_code)

    except Exception as e:
        error_msg = f"Ошибка: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)

        try:
            log_path = os.path.join(os.path.dirname(sys.executable), 'error.log')
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(error_msg)
            print(f"\nОшибка сохранена в: {log_path}")
        except Exception:
            pass

        input("\nНажмите Enter для выхода...")
        sys.exit(1)

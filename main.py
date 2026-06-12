import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from core.ollama_manager import start_ollama_service

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 自动检测并启动 Ollama 服务
    ok, msg = start_ollama_service()
    if not ok:
        QMessageBox.critical(None, "环境检测", f"Ollama 服务异常：{msg}")
        sys.exit(1)

    # 启动主窗口
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
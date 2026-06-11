import sys
from PyQt6.QtWidgets import QApplication
from db.database import init_db, init_default_questions
from ui.main_window import MainWindow

if __name__ == "__main__":
    # 初始化数据库+内置题库
    init_db()
    init_default_questions()

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
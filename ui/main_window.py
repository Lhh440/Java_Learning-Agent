from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QTabWidget, QListWidget, QListWidgetItem, QMessageBox
)
import json
import os

from db.database import add_chat_record, add_error_code, get_all_errors
from core.agent_core import get_agent_reply
from core.ollama_manager import stop_ollama_process
from core.text_filter import clean_markdown

CFG_PATH = "window_cfg.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Java学习助手Agent")
        self.resize(1000, 700)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.create_code_tab()
        self.create_qa_tab()
        self.create_error_tab()
        self.create_exam_tab()

        # 加载窗口记忆
        self.load_window_cfg()

    def load_window_cfg(self):
        if os.path.exists(CFG_PATH):
            try:
                with open(CFG_PATH, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    x = cfg.get("x", 100)
                    y = cfg.get("y", 100)
                    w = cfg.get("w", 1000)
                    h = cfg.get("h", 700)
                    self.setGeometry(x, y, w, h)
            except Exception:
                pass

    def save_window_cfg(self):
        geo = self.geometry()
        cfg = {
            "x": geo.x(),
            "y": geo.y(),
            "w": geo.width(),
            "h": geo.height()
        }
        with open(CFG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

    def closeEvent(self, event):
        self.save_window_cfg()
        stop_ollama_process()
        event.accept()

    # ========== 代码纠错标签页 ==========
    def create_code_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("粘贴你的Java代码...")
        self.code_output = QTextEdit()
        self.code_output.setReadOnly(True)

        btn_layout = QHBoxLayout()
        self.btn_code_run = QPushButton("解析代码 & 纠错")
        self.btn_code_save = QPushButton("保存到错题本")
        self.btn_code_clear = QPushButton("清空输入")

        btn_layout.addWidget(self.btn_code_run)
        btn_layout.addWidget(self.btn_code_save)
        btn_layout.addWidget(self.btn_code_clear)

        layout.addWidget(QLabel("Java代码输入区"))
        layout.addWidget(self.code_input)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("AI解析结果"))
        layout.addWidget(self.code_output)

        self.btn_code_run.clicked.connect(self.on_code_analyze)
        self.btn_code_clear.clicked.connect(lambda: self.code_input.clear())
        self.btn_code_save.clicked.connect(self.save_code_error)

        self.tab_widget.addTab(tab, "代码纠错")

    def on_code_analyze(self):
        code = self.code_input.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, "提示", "请输入Java代码")
            return
        self.code_output.setPlainText("AI思考中...")
        raw = get_agent_reply(f"分析下面Java代码错误，给出修正和讲解：\n{code}")
        safe_text = clean_markdown(raw)
        self.code_output.setPlainText(safe_text)

    def save_code_error(self):
        code = self.code_input.toPlainText().strip()
        ans = self.code_output.toPlainText().strip()
        if not code or not ans:
            QMessageBox.warning(self, "提示", "代码或解析结果不能为空")
            return
        add_error_code(code, ans, "", "")
        QMessageBox.information(self, "成功", "已存入错题本")

    # ========== 问答标签页 ==========
    def create_qa_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.qa_input = QTextEdit()
        self.qa_input.setPlaceholderText("输入你的Java问题...")
        self.qa_output = QTextEdit()
        self.qa_output.setReadOnly(True)

        btn_layout = QHBoxLayout()
        btn_send = QPushButton("提问")
        btn_clear_ctx = QPushButton("清空输出")
        btn_layout.addWidget(btn_send)
        btn_layout.addWidget(btn_clear_ctx)

        layout.addWidget(QLabel("问题"))
        layout.addWidget(self.qa_input)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("回答"))
        layout.addWidget(self.qa_output)

        btn_send.clicked.connect(self.on_qa_send)
        btn_clear_ctx.clicked.connect(lambda: self.qa_output.clear())
        self.tab_widget.addTab(tab, "知识点问答")

    def on_qa_send(self):
        q = self.qa_input.toPlainText().strip()
        if not q:
            return
        self.qa_output.setPlainText("思考中...")
        raw = get_agent_reply(q)
        safe = clean_markdown(raw)
        self.qa_output.setPlainText(safe)
        add_chat_record(q, "user")
        add_chat_record(safe, "assistant")

    # ========== 错题本标签页 ==========
    def create_error_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.error_list = QListWidget()
        refresh_btn = QPushButton("刷新错题")
        layout.addWidget(refresh_btn)
        layout.addWidget(self.error_list)
        refresh_btn.clicked.connect(self.load_errors)
        self.load_errors()
        self.tab_widget.addTab(tab, "错题本")

    def load_errors(self):
        self.error_list.clear()
        data = get_all_errors()
        for item in data:
            _, code, err_desc, fix_code, knowledge, ctime = item
            item_w = QListWidgetItem(f"{ctime}\n代码片段：{code[:60]}...")
            self.error_list.addItem(item_w)

    # ========== 刷题标签页（预留） ==========
    def create_exam_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("刷题模块（V2拓展）"))
        self.tab_widget.addTab(tab, "刷题练习")
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QListWidget, QListWidgetItem, QMessageBox
)
from db.database import add_chat_record, add_error_code, get_all_errors, get_random_question
from core.agent_core import get_agent_reply, clear_context

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Java学习助学Agent")
        self.resize(1000, 700)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.create_code_tab()
        self.create_qa_tab()
        self.create_error_tab()
        self.create_exam_tab()

    # 1 代码纠错标签页
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
        self.btn_code_save.clicked.connect(self.on_save_error)

        self.tab_widget.addTab(tab, "代码纠错")

    def on_code_analyze(self):
        code = self.code_input.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, "提示", "请输入Java代码！")
            return
        reply, chat_type = get_agent_reply(code)
        self.code_output.setPlainText(reply)
        add_chat_record(code, "user", chat_type)
        add_chat_record(reply, "ai", chat_type)

    def on_save_error(self):
        code = self.code_input.toPlainText().strip()
        result = self.code_output.toPlainText().strip()
        if not code or not result:
            QMessageBox.warning(self, "提示", "代码或解析结果不能为空")
            return
        add_error_code(code, result, "", "Java代码错误")
        QMessageBox.information(self, "成功", "已存入错题本")
        self.refresh_error_list()

    # 2 知识点问答
    def create_qa_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.qa_input = QTextEdit()
        self.qa_input.setPlaceholderText("输入Java问题，例如：什么是重载和重写？")
        self.qa_output = QTextEdit()
        self.qa_output.setReadOnly(True)

        btn_layout = QHBoxLayout()
        self.btn_qa_send = QPushButton("提问")
        self.btn_qa_clear = QPushButton("清空对话上下文")

        btn_layout.addWidget(self.btn_qa_send)
        btn_layout.addWidget(self.btn_qa_clear)

        layout.addWidget(QLabel("你的问题"))
        layout.addWidget(self.qa_input)
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("AI解答"))
        layout.addWidget(self.qa_output)

        self.btn_qa_send.clicked.connect(self.on_qa_ask)
        self.btn_qa_clear.clicked.connect(self.on_qa_clear)

        self.tab_widget.addTab(tab, "知识点问答")

    def on_qa_ask(self):
        q = self.qa_input.toPlainText().strip()
        if not q:
            QMessageBox.warning(self, "提示", "请输入问题")
            return
        reply, chat_type = get_agent_reply(q)
        self.qa_output.append(f"【你】{q}\n【AI】{reply}\n\n")
        add_chat_record(q, "user", chat_type)
        add_chat_record(reply, "ai", chat_type)

    def on_qa_clear(self):
        self.qa_input.clear()
        self.qa_output.clear()
        clear_context()

    # 3 错题本
    def create_error_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.error_list = QListWidget()
        layout.addWidget(QLabel("历史错题（点击查看详情）"))
        layout.addWidget(self.error_list)
        self.refresh_error_list()
        self.error_list.itemClicked.connect(self.show_error_detail)
        self.tab_widget.addTab(tab, "错题本")

    def refresh_error_list(self):
        self.error_list.clear()
        err_list = get_all_errors()
        for item in err_list:
            display = f"ID:{item[0]} | 分类:{item[4]} | 时间:{item[5]}"
            list_item = QListWidgetItem(display)
            list_item.setData(100, item)
            self.error_list.addItem(list_item)

    def show_error_detail(self, item):
        data = item.data(100)
        code = data[1]
        desc = data[2]
        QMessageBox.information(self, "错题详情", f"【错误代码】\n{code}\n\n【解析】\n{desc}")

    # 4 刷题练习
    def create_exam_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.que_label = QLabel("点击「下一题」开始刷题")
        self.ans_edit = QTextEdit()
        self.ans_edit.setPlaceholderText("写下你的答案")
        self.result_label = QLabel("作答结果：")

        btn_layout = QHBoxLayout()
        self.btn_next_que = QPushButton("下一题")
        self.btn_submit_ans = QPushButton("提交答案")
        btn_layout.addWidget(self.btn_next_que)
        btn_layout.addWidget(self.btn_submit_ans)

        layout.addWidget(self.que_label)
        layout.addWidget(QLabel("你的作答"))
        layout.addWidget(self.ans_edit)
        layout.addLayout(btn_layout)
        layout.addWidget(self.result_label)

        self.current_que = None
        self.btn_next_que.clicked.connect(self.load_next_question)
        self.btn_submit_ans.clicked.connect(self.check_answer)
        self.tab_widget.addTab(tab, "刷题练习")

    def load_next_question(self):
        q = get_random_question()
        if not q:
            self.que_label.setText("暂无题库")
            return
        self.current_que = q
        self.que_label.setText(f"题目：{q[1]}")
        self.ans_edit.clear()
        self.result_label.setText("作答结果：")

    def check_answer(self):
        if not self.current_que:
            QMessageBox.warning(self, "提示", "请先获取题目")
            return
        user_ans = self.ans_edit.toPlainText().strip()
        std = self.current_que[2]
        self.result_label.setText(f"【参考答案】\n{std}\n【你的回答】\n{user_ans}")
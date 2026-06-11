import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "java_study.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 对话记录
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        role TEXT NOT NULL,
        chat_type TEXT,
        create_time TEXT
    )
    ''')

    # 错题表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS error_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        java_code TEXT NOT NULL,
        error_desc TEXT,
        fix_code TEXT,
        knowledge TEXT,
        create_time TEXT
    )
    ''')

    # 题库
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS java_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        knowledge TEXT,
        q_type TEXT
    )
    ''')

    conn.commit()
    conn.close()

# 对话记录
def add_chat_record(content, role, chat_type="question"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO chat_records (content, role, chat_type, create_time) VALUES (?,?,?,?)",
        (content, role, chat_type, now)
    )
    conn.commit()
    conn.close()

# 错题操作
def add_error_code(java_code, error_desc, fix_code, knowledge):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO error_codes (java_code, error_desc, fix_code, knowledge, create_time) VALUES (?,?,?,?,?)",
        (java_code, error_desc, fix_code, knowledge, now)
    )
    conn.commit()
    conn.close()

def get_all_errors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM error_codes ORDER BY id DESC")
    res = cursor.fetchall()
    conn.close()
    return res

# 题库初始化
def init_default_questions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM java_questions")
    questions = [
        ("Java中main方法的标准写法是什么？", "public static void main(String[] args){}", "Java基础语法", "essay"),
        ("Java面向对象三大特性是什么？", "封装、继承、多态", "面向对象", "essay"),
        ("== 和 equals() 区别？", "==比较内存地址；equals默认比较地址，可重写比较内容", "字符串", "essay")
    ]
    cursor.executemany(
        "INSERT INTO java_questions (question, answer, knowledge, q_type) VALUES (?,?,?,?)",
        questions
    )
    conn.commit()
    conn.close()

def get_random_question():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM java_questions ORDER BY RANDOM() LIMIT 1")
    res = cursor.fetchone()
    conn.close()
    return res
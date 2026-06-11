```markdown
# Java Learning Agent
轻量级离线Java学习AI助学工具，基于Python+PyQt6+Ollama开发，纯CPU运行、本地数据存储，专为Java自学新手打造。

## ✨ 核心功能
1. **Java代码纠错**：粘贴代码自动定位语法/逻辑错误，输出完整可运行修正代码
2. **知识点智能答疑**：覆盖Java基础、面向对象、集合、异常、IO、多线程等全部入门内容
3. **本地错题本**：一键保存易错代码与解析，永久本地归档，随时回看
4. **内置题库刷题**：随机抽取Java基础习题，作答后对照标准答案复盘
5. **隐私安全**：所有对话、代码、错题仅保存在本地SQLite数据库，不上传任何云端
6. **离线可用**：依托Ollama本地大模型，断网也能正常使用

## 🖥️ 运行环境要求
- Python 3.10 及以上版本
- Ollama 客户端（Windows/macOS/Linux均可）
- 推荐模型：`qwen2.5:3b`（低配机器可选用 `phi3:mini`）
- 纯CPU即可流畅运行，不需要独立显卡

## 🚀 快速启动教程
### 第一步：克隆项目 & 安装Python依赖
```bash
git clone https://github.com/LHH440/java-learning-agent.git
cd java-learning-agent

# 安装依赖库
pip install -r requirements.txt
```

### 第二步：拉取本地大模型
二选一执行，推荐Qwen2.5 3B，中文+代码理解更强
```bash
# 方案1：综合性能更好（推荐）
ollama pull qwen2.5:3b

# 方案2：低配电脑超轻量备选
# ollama pull phi3:mini
```

### 第三步：启动程序
```bash
python main.py
```
首次运行会自动初始化SQLite数据库与内置基础题库，无需手动操作。

## 📁 项目目录结构
```
java-learning-agent/
├── assets/            # 存放截图、图标等静态资源
├── core/              # 核心逻辑层
│   ├── __init__.py
│   ├── agent_core.py  # 轻量Agent会话、提示词、输入识别
│   └── llm_client.py  # Ollama接口统一封装
├── db/                # 数据库模块
│   ├── __init__.py
│   └── database.py   # SQLite建表、增删改查方法
├── ui/                # PyQt6图形界面
│   ├── __init__.py
│   └── main_window.py # 四标签页GUI窗口
├── .gitignore        # Git忽略配置
├── LICENSE           # MIT开源协议
├── main.py           # 程序入口启动文件
├── README.md         # 项目说明文档
└── requirements.txt  # Python依赖清单
```

## 📌 软件四大模块使用说明
### 1. 代码纠错
粘贴有问题的Java代码，点击解析，AI会逐行排查错误并给出修改方案，满意后可一键存入错题本。

### 2. 知识点问答
输入你不懂的Java概念（例如：重载和重写的区别），AI用通俗语言讲解并附带简单示例；支持连贯多轮对话。

### 3. 错题本
所有保存的错题会列表展示，点击条目可查看完整错误代码与解析，方便周期性复盘。

### 4. 刷题练习
随机调取内置Java基础题，写完答案提交即可对照标准答案自查，巩固基础知识点。

## ⚙️ 模型切换说明
如果你使用`phi3:mini`模型，打开 `core/llm_client.py` 修改这一行：
```python
MODEL_NAME = "qwen2.5:3b"
# 改为
MODEL_NAME = "phi3:mini"
```

## 📄 开源协议
本项目基于 **MIT License** 开源，你可以自由使用、修改、分发，商用也无需额外授权。

## 💡 后续可拓展方向
- 新增Java代码语法高亮
- 扩充海量Java专项题库
- 增加对话记录导出TXT功能
- 暗黑/浅色双主题切换
- 支持导出错题文档
```

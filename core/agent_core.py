JAVA_CODE_KEYWORDS = {
    "public", "class", "static", "void", "main", "String",
    "int", "boolean", "if", "for", "while", "{", "}", ";"
}
MAX_CONTEXT = 5
chat_context = []

def is_java_code(input_text: str) -> bool:
    text = input_text.lower()
    for kw in JAVA_CODE_KEYWORDS:
        if kw in text:
            return True
    return False

def build_prompt(user_input: str, is_code: bool) -> str:
    rule = """
强制硬性规则，必须严格遵守，违反规则会视为回答错误：
1、全程只能输出纯文本，绝对禁止出现任何markdown标记：#、##、###、```、`、*、-、>、```java 全部不允许出现
2、分层只用中文序号：一、二、三；子项用1、2、3；细分用（1）（2）
3、Java代码直接原样换行平铺展示，不要任何包裹符号
4、段落之间空一行分隔，不要多余符号、分割线
5、不许输出反引号、代码块标识、标题符号
"""
    if is_code:
        prompt = f"""{rule}
你是Java入门辅导老师，任务：
1、找出这段Java代码所有语法、逻辑、运行错误
2、给出完整、可直接运行的修正后代码
3、用零基础能听懂的大白话，逐条讲解错误原因和对应知识点

用户代码：
{user_input}
"""
    else:
        prompt = f"""{rule}
你是零基础Java辅导老师，通俗讲解Java问题，搭配简单代码示例，标注高频易错点
{user_input}
"""
    return prompt

def get_agent_reply(user_input: str) -> tuple[str, str]:
    global chat_context
    code_flag = is_java_code(user_input)
    chat_type = "code" if code_flag else "question"

    current_msg = {"role": "user", "content": build_prompt(user_input, code_flag)}
    chat_context.append(current_msg)

    if len(chat_context) > MAX_CONTEXT * 2:
        chat_context = chat_context[-MAX_CONTEXT * 2:]

    from core.llm_client import call_ollama
    ai_reply = call_ollama(chat_context)
    chat_context.append({"role": "assistant", "content": ai_reply})
    return ai_reply, chat_type

def clear_context():
    global chat_context
    chat_context = []
import re

def clean_markdown(text: str) -> str:
    """清除所有 Markdown 格式符号，保证界面展示整洁"""
    if not text:
        return ""
    # 移除多行代码块
    text = re.sub(r"```[\s\S]*?```", "", text)
    # 移除行内反引号
    text = re.sub(r"`+", "", text)
    # 移除标题 #
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    # 移除列表符号 * -
    text = re.sub(r"^[\*\-]\s*", "", text, flags=re.MULTILINE)
    # 移除加粗符号
    text = re.sub(r"\*\*", "", text)
    # 压缩多余空行
    text = re.sub(r"\n{3,}", r"\n\n", text)
    return text.strip()
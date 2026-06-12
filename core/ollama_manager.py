import socket
import subprocess
import os
import time

OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
OLLAMA_CMD = ["ollama", "serve"]

def is_port_in_use(host: str, port: int) -> bool:
    """检测端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0

def start_ollama_service():
    """后台启动 ollama serve"""
    if is_port_in_use(OLLAMA_HOST, OLLAMA_PORT):
        return True, "Ollama 服务已运行"

    try:
        # 后台启动，不弹出黑框
        subprocess.Popen(
            OLLAMA_CMD,
            env=dict(os.environ, OLLAMA_HOST=f"{OLLAMA_HOST}:{OLLAMA_PORT}"),
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        # 等待服务启动
        for _ in range(10):
            time.sleep(0.5)
            if is_port_in_use(OLLAMA_HOST, OLLAMA_PORT):
                return True, "Ollama 服务启动成功"
        return False, "Ollama 启动超时"
    except Exception as e:
        return False, f"启动失败：{str(e)}"

def stop_ollama_process():
    """关闭 ollama 进程"""
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", "ollama.exe"],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    except:
        return False
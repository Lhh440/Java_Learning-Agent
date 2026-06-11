@echo off
chcp 65001
echo 正在启动Ollama本地API服务(127.0.0.1:11434)
taskkill /f /im ollama.exe >nul 2>&1
set OLLAMA_HOST=127.0.0.1:11434
ollama serve
pause
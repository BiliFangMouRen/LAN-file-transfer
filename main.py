import subprocess
import os

def start_app():
    """启动 Flask 应用."""
    print("正在启动 Flask 应用...")
    subprocess.Popen(['python', 'app.py'])

def start_uploader():
    """启动 GUI 上传工具."""
    print("正在启动 GUI 上传工具...")
    subprocess.Popen(['python', 'uploader.py'])

if __name__ == "__main__":
    start_app()
    start_uploader()
    print("所有应用已启动。") 
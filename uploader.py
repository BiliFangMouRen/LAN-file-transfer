import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os

SERVER_URL = 'http://localhost:8080/upload'

def upload_file():
    filename = filedialog.askopenfilename()
    if filename:
        try:
            with open(filename, 'rb') as f:
                files = {'file': (os.path.basename(filename), f)}
                response = requests.post(SERVER_URL, files=files)
                response.raise_for_status()  # 检查请求是否成功
                messagebox.showinfo("上传成功", "文件已成功上传到服务器！")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("上传失败", f"文件上传失败: {e}")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {e}")

root = tk.Tk()
root.title("文件上传工具")

upload_button = tk.Button(root, text="选择文件并上传", command=upload_file)
upload_button.pack(padx=20, pady=20)

root.mainloop()
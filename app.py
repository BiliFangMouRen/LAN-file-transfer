from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from werkzeug.utils import secure_filename
import shutil
import datetime
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'downloads'  # 文件上传后保存的目录，与下载目录相同
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在并清空
if os.path.exists(UPLOAD_FOLDER):
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
else:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return redirect(url_for('list_files'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/files')
def list_files():
    files_data = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # 获取文件的修改时间（这里可以作为上传时间）
        modified_time = os.path.getmtime(file_path)
        # 将时间戳转换为 datetime 对象
        upload_time = datetime.datetime.fromtimestamp(modified_time)
        files_data.append({'filename': filename, 'upload_time': upload_time})

    # 按照上传时间升序排序
    files_data.sort(key=lambda x: x['upload_time'])

    return render_template('files.html', files_data=files_data)

if __name__ == '__main__':
    subprocess.Popen(['python', 'uploader.py'])
    app.run(debug=False, port=8080) 
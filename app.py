from flask import Flask, redirect, url_for, render_template, request
import os
import send_alert_email

app = Flask(__name__)

UPLOAD_PATH = 'uploads'


#메인 페이지
@app.route('/')
def index():
    return render_template('index.html')


#파일 업로드 겁사
@app.route('/upload', methods=['POST'])
def upload():
    if "file" not in request.files:
        return "파일이 없습니다.", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "파일이 선택되지 않았습니다.", 400
    
    #파일 저장
    file.save(os.path.join(UPLOAD_PATH, file.filename))

    #업로드 후 결과 페이지로 리다이렉트
    return redirect(url_for('result'))


#결과 페이지
@app.route('/result')
def result():
    return render_template("result.html")


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
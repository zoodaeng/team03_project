from flask import Flask, redirect, url_for, render_template, request
import os
import send_alert_email, privacy_detector

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
    file_path = os.path.join(UPLOAD_PATH, file.filename)
    file.save(file_path)
    print(file_path)
    
    #업로드 후 결과 페이지로 리다이렉트


#결과 페이지
@app.route('/result', methods=['POST'])
def result():
    if "file" not in request.files:
        return "파일이 없습니다.", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "파일이 선택되지 않았습니다.", 400
    
    #파일 저장
    file_path = os.path.join(UPLOAD_PATH, file.filename)
    file.save(file_path)
    print(file_path)

    #민감정보 탐지 결과(딕셔너리) result 변수에 저장
    result = privacy_detector.privacy_detector(file_path)
    print(result)

    #결과 메일로 전송
    send_alert_email.send_alert_email(file.name, result)

    return render_template("result.html")


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
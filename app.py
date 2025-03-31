from flask import Flask, redirect, render_template, request
import os
import send_alert_email, check_sensitive_info

app = Flask(__name__)

UPLOAD_PATH = 'uploads'


#메인 페이지(파일 업로드 페이지)
@app.route('/')
def index():
    return render_template('index.html')


#결과 페이지
@app.route('/result', methods=['POST'])
def result():
    
    #파일 미선택 시 예외 처리
    if "file" not in request.files:
        return "파일이 없습니다.", 400
    file = request.files["file"]
    if file.filename == "":
        return "파일이 선택되지 않았습니다.", 400
    
    #업로드 파일 저장
    file_path = os.path.join(UPLOAD_PATH, file.filename)
    file.save(file_path)
    print(f'파일이 업로드 되었습니다: {file_path}\n')

    #민감한 정보 탐지 및 결과값 저장
    #personal_info 변수: 개인정보(연락처, 이메일, ...)
    #sensitive_info 변수: 민감정보(종교, 주량, ...)
    personal_info, sensitive_info = check_sensitive_info.check_sensitive_info(file_path)
    
    #탐지된 정보가 있을 경우, 메일 전송 실행
    if personal_info != False:
        send_alert_email.send_alert_email(file.filename, personal_info)

    return render_template("result.html")


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
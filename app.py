from flask import Flask, redirect, render_template, request
import os, itertools
from db_utils import connect_to_db, save_detection_result  # db_utils.py에서 함수 import
import send_alert_email, check_sensitive_info

app = Flask(__name__)

UPLOAD_PATH = 'uploads'

## MongoDB 연결
collection = connect_to_db()

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
    #results 변수: 개인정보(연락처, 이메일, ...)
    #add_info 변수: 민감정보(종교, 주량, ...)
    results, add_info = check_sensitive_info.check_sensitive_info(file_path)
    print("results:", results)

    # MongoDB에 데이터 저장
    if collection is not None:
        save_detection_result(collection, file.filename, file_path, results)  # 올바른 데이터를 전달
        print("DB 저장 완료")   # 데이터 저장 성공, DB 저장 완료
    else:
        return "MongoDB 연결 오류. 데이터를 저장할 수 없습니다.", 500

     # 길이가 다른 리스트도 None으로 채워서 zip하기(빈 값은 "없음"으로 채움)
    if all(len(results[key]) == 0 for key in results):
        results_zipped = False
    else:
        results_zipped = list(itertools.zip_longest(
            results["email"], results["person"], results["num"], results["addr"], results["card"],
            fillvalue="없음"
        ))
        #탐지된 정보가 있을 경우, 메일 전송 실행
        send_alert_email.send_alert_email(file.filename, results)
        
    return render_template("result.html", results=results_zipped)


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
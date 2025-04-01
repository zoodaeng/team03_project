# 📄 입사지원서 파일 업로드 및 민감정보 탐지 안내 서비스

---
 
## 📌 개요
- 웹 페이지에서 지원자가 업로드한 HWP 파일의 개인정보와 민감정보를 탐지하고 결과를 안내한 뒤, 보안 담당자에게 알림을 보내는 시스템

---

## 🛠️ 주요 기능과 담당 역할

1. **파일 업로드**  
   - 웹 페이지에서 사용자가 HWP 파일을 업로드
   - Flask 서버에서 파일을 수신 및 저장

2. **민감정보 탐지**  
   - 업로드된 HWP 파일의 텍스트를 추출
   - 정규표현식을 활용하여 주민번호, 연락처, 주소 등의 민감정보 탐지

3. **검토 결과 안내**  
   - 탐지된 민감정보 내용을 웹 페이지에서 사용자에게 안내

4. **보안 담당자 알림**  
   - SMTP를 활용하여 탐지 결과를 보안 담당자에게 이메일로 전송
     
5. **데이터베이스 저장**  
   - 업로드된 파일명, 업로드 시간, 탐지 결과 등을 MongoDB에 저장

---

## 📂 프로젝트 구조
```
📦 team03_project
├── 📂 static
│   ├── 📜 style.css            # CSS 스타일 파일
├── 📂 templates
│   ├── 📜 index.html           # 파일 업로드 웹 페이지
│   ├── 📜 rsult.html           # 민감정보 탐지 결과 웹 페이지
├── 📂 uploads                  # 업로드 파일 저장 폴더
├── 📜 app.py                   # Flask 서버 및 주요 로직
├── 📜 check_sensitive_info.py  # 민감정보 탐지 함수
├── 📜 send_alert_email.py      # 보안 담당자 이메일 전송 함수
└── 📜 db_utils.py              # 결과값 DB 저장 함수

```



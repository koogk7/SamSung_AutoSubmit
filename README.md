# SamSung_AutoSubmit
🇰🇷💼 삼성전자 무선사업부 3급 공채 지원시 학부수강과목을 자동으로 기입해주는 프로그램

<img width="757" alt="스크린샷 2019-05-29 오후 9 46 22" src="https://user-images.githubusercontent.com/48513360/58558270-5323ca00-825b-11e9-871d-927ce5cd53c5.png">

[영상보기](https://www.youtube.com/watch?v=bPMYSqB1dVQ&t=3s)

## How To build?
1. student_id, student_pw의 부산대 계정정보 입력
2. samsung_id, samsung_pw의 삼섬채용 계정정보 입력
3. 가상환경 on `source venv/bin/activate`
4. python Build `python3 AutoSubmit.py`

## 
* 맥 환경 기준으로 작성되었기에 윈도우에서 빌드시,[여기](https://chromedriver.storage.googleapis.com/index.html?path=76.0.3809.126/)에서 크롬 드라이버를 재설치 해야합니다. 다운받은 크롬 드라이버는 utill 디렉토리 아래의 위치시켜 주세요
* 지원서가 작성이 된 상태에서 빌드되어야 합니다.
* 성적 입력중 프로그램이 죽을 경우 다시 빌드하면, 입력되지 않은 과목부터 순차입력됩니다.
* 성적 입력이 완료 후( 5 ~ 15분 사이) 반드시 과목과 과목 수를 확인하시길 권장드립니다.
* 테스트용 소스코드로 환경에 따라 동작하지 않을 수 있습니다.


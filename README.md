### 프로젝트 목적
---
벨로그에서 조회수를 확인할 때, 각 글마다 일일이 들어가서 보는 것이 번거로워 한 번에 모든 글의 조회수를 확인할 수 있도록 하기 위해 이 프로젝트를 만듦

<br>
<br>

### 사용 방법
---
1. 소스 코드 다운로드
1. 필요한 패키지 설치
    - VSCode 등으로 프로젝트 열고, VSCode의 터미널에서 `pip install -r requirements.txt` 입력해 환경에 맞는 패키지 다운로드
    - 아니면 터미널에서 직접 프로젝트 디렉터리로 이동한 후 `pip install -r requirements.txt` 입력
1. app.py 실행
1. http://localhost:5000 으로 접속
1. Velog username 입력
    - 내 벨로그 주소에서 @ 뒤에 오는 부분
1. Access Token 가져오기
    - 내 벨로그에서 F12(개발자 도구) → 응용 프로그램(애플리케이션) 탭 → access_token의 값 복사
1. Access Token 입력
    - http://localhost:5000 의 Enter your access token에 붙여넣기
    - 주의 사항 : access token은 유출되면 보안에 문제가 있을 수 있으니 주의해서 다뤄야 함
1. python 터미널에서 ctrl+c로 서비스 종료
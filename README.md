# Backend FLASK 사용법

### API KEY 꼭 지우고 푸시!

## Setup

1. brew로 pip, python, openai 설치.

2. 레포 클론

3. 레포로 이동

   ```bash
   $ cd openai-quickstart-python
   ```

4. 가상환경 생성

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. 터미널에 입력 후 필요한 패키지 다운

   ```bash
   $ pip install -r requirements.txt
   ```

6. 환경변수 파일 (근데 안해도 됨)

   ```bash
   $ cp .env.example .env
   ```

7. API key 넣기

8. 돌리기 ! (꼭 4번에서 생성한 가상환경 진입하고 run 해야 함)

   ```bash
   $ flask run
   ```

9. 깃에 푸시할 때/개발 종료 후에 가상환경 종료해야 함.

   ```bash
   $ deactivate
   ```

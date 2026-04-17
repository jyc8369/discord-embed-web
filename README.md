# Discord Embed Web Server

Flask 기반 웹 애플리케이션으로 Discord OAuth2 로그인, 임베드 전송, 수정, 삭제 기능을 제공합니다. 사용자는 자신의 임베드 기록을 확인하고 기록을 통해 임베드를 편집하거나 삭제할 수 있습니다.

## 구조

- `app/` - Flask 애플리케이션 소스
  - `config.py` - 환경 변수 로드
  - `db.py` - SQLAlchemy 데이터베이스 모델
  - `discord_oauth.py` - Discord OAuth2 인증 처리
  - `discord_client.py` - Discord 메시지 REST API 호출
  - `services/embeds.py` - 기록 CRUD 로직
  - `routes.py` - Flask 라우트 정의
  - `web.py` - 앱 실행 엔트리포인트
  - `templates/` - HTML 템플릿
- `data/` - SQLite 데이터베이스 저장소
- `requirements.txt` - Python 의존성
- `.env.example` - 환경 변수 샘플

## 설치

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 설정

루트에 `.env` 파일을 생성하고 다음 값을 설정하세요:

```ini
SECRET_KEY=change-me
DATABASE_URL=sqlite:///data/app.db
DISCORD_CLIENT_ID=your_client_id
DISCORD_CLIENT_SECRET=your_client_secret
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=target_channel_id
DISCORD_REDIRECT_URI=http://localhost:5000/callback
```

## 실행

```bash
python app/web.py
```

## 사용 흐름

1. `/login`으로 Discord OAuth2 로그인
2. 홈 페이지에서 임베드 생성
3. `/history`에서 사용자 임베드 기록 확인
4. 기록 선택 후 수정/삭제


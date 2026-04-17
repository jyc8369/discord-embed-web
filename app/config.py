import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def normalize_sqlite_url(url: str) -> str:
    if url.startswith("sqlite:///"):
        db_path = Path(url[10:])
        if not db_path.is_absolute():
            db_path = BASE_DIR / db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path.as_posix()}"
    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = normalize_sqlite_url(
        os.getenv(
            "DATABASE_URL",
            f"sqlite:///{(BASE_DIR / 'data' / 'app.db').as_posix()}"
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
    DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
    DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:5000/callback")
    DISCORD_API_BASE_URL = "https://discord.com/api"
    OAUTH_SCOPE = "identify"

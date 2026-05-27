from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_DIR = BASE_DIR / "env"
LOG_DIR = BASE_DIR / "logs"
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "upload"
SCRIPT_DATA_DIR = BASE_DIR / "app" / "scripts" / "data"
ALEMBIC_VERSION_DIR = BASE_DIR / "app" / "alembic" / "versions"
BANNER_FILE = BASE_DIR / "banner.txt"
BANNER_TEXT_FILE = BASE_DIR / "banner.text"

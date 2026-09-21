import os

BASE_URL: dict[str, str] = {
    "gymshark": "https://www.gymshark.com/",
    "alo": "",
    "vuori": "",
}

LOG_LEVEL = "INFO"
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3

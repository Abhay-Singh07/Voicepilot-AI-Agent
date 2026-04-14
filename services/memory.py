import os
from datetime import datetime
from config import HISTORY_DIR, HISTORY_FILE


def ensure_memory():
    os.makedirs(HISTORY_DIR, exist_ok=True)


def save_memory(action: str):
    ensure_memory()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {action}\n")


def load_memory(limit=20):
    ensure_memory()

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    return [line.strip() for line in lines[-limit:]]


def clear_memory():
    ensure_memory()

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write("")
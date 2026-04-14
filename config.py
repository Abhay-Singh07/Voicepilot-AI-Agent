import os
from pathlib import Path
from dotenv import load_dotenv



BASE_DIR = Path(__file__).resolve().parent


load_dotenv(BASE_DIR / ".env")



APP_NAME = "VoicePilot AI Agent"


# MODELS

LLM_MODEL = "llama-3.1-8b-instant"
WHISPER_MODEL = "base"


# PATHS

OUTPUT_DIR = "output"
HISTORY_DIR = "history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "log.txt")


# API

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8000
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# =========================
# SECRETS
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in .env")

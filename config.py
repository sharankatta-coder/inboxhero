import os

class Config:
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OUTBOX_DIR = "outbox"
    TRACE_FILE = "trace.jsonl"
    PREFS_FILE = "prefs.json"

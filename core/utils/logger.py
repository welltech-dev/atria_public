import json
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "conversas.jsonl"

def salvar_conversa(login_usuario, role, content):
    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "login": login_usuario,
        "role": role,
        "content": content
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

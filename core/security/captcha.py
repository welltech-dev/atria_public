import jwt
import time
import secrets
import hashlib

from flask import request
from jwt import ExpiredSignatureError, InvalidTokenError
from core.config.config import SECRET_KEY, CAPTCHA_EXP_SECONDS

# memória simples anti-replay - migrar pra Redis depois
USED_TOKENS = set()


def _fingerprint():
    """Cria fingerprint leve do cliente"""
    ip = request.remote_addr or ""
    ua = request.headers.get("User-Agent", "")
    raw = f"{ip}:{ua}"
    return hashlib.sha256(raw.encode()).hexdigest()


def generate_captcha():
    a = secrets.randbelow(9) + 1
    b = secrets.randbelow(9) + 1
    op = secrets.choice(["+", "-", "*"])

    if op == "+":
        answer = a + b
    elif op == "-":
        a, b = max(a, b), min(a, b)
        answer = a - b
    else:
        answer = a * b

    payload = {
        "answer": answer,
        "fp": _fingerprint(),  # substitui IP puro
        "iat": int(time.time()),
        "exp": int(time.time()) + CAPTCHA_EXP_SECONDS,
        "jti": secrets.token_hex(16)  #  id único - anti-replay
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return {
        "question": f"{a} {op} {b}",
        "token": token
    }


def validate_captcha(token, user_answer):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # anti-replay
        jti = payload.get("jti")
        if not jti or jti in USED_TOKENS:
            return False

        # valida fingerprint
        if payload.get("fp") != _fingerprint():
            return False

        # valida resposta
        if "answer" not in payload:
            return False

        try:
            user_answer_int = int(user_answer)
        except (ValueError, TypeError):
            return False

        if user_answer_int != int(payload["answer"]):
            return False

        # NÃO marca como usado aqui - será marcado no login
        return True

    except ExpiredSignatureError:
        return False

    except InvalidTokenError:
        return False

    except Exception as e:
        print("Erro captcha:", e)
        return False


def consume_captcha(token):
    """Marca um token de captcha como usado (após login bem-sucedido)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        jti = payload.get("jti")
        if jti:
            USED_TOKENS.add(jti)
        return True
    except:
        return False
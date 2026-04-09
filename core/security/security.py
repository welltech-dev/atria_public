import hmac
import secrets
import jwt

from functools import wraps
from flask import (
    session, url_for, redirect,
    abort, request
)

from jwt import ExpiredSignatureError, InvalidTokenError
from core.config.config import SECRET_KEY

# LOGIN REQUIRED
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("auth"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated

# CSRF
def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def validate_csrf():
    token_form = request.form.get("csrf_token")
    
    if not token_form and request.is_json:
        token_form = request.get_json().get("csrf_token")
    
    token_session = session.get("csrf_token")

    # Sem token → bloqueia direto
    if not token_form or not token_session:
        abort(403)

    # 1 - valida CSRF da sessão (como já era)
    if token_session and hmac.compare_digest(token_form, token_session):
        return True

    # 2 - valida token JWT do captcha
    try:
        payload = jwt.decode(token_form, SECRET_KEY, algorithms=["HS256"])

        # valida se é realmente um token de captcha
        if "answer" in payload and "exp" in payload:
            return True

    except ExpiredSignatureError:
        pass
    except InvalidTokenError:
        pass
    except Exception:
        pass

    # qualquer outro caso → bloqueia
    abort(403)


EXEMPT_ROUTES = ["login", "register", "captcha.get_captcha", "captcha.captcha_verify", "auth.logout"]


def csrf_protect():
    if request.method == "POST" and request.endpoint not in EXEMPT_ROUTES:
        validate_csrf()


def inject_csrf():
    return dict(csrf_token=generate_csrf_token())

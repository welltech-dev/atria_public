<<<<<<< HEAD
import random

from core.security.security import login_required

from flask import (
    session, request,
    url_for, redirect,
    Blueprint
)

captcha_bp = Blueprint("captcha", __name__)

# CAPTCHA
@captcha_bp.route("/captcha")
def captcha():

    a = random.randint(1, 9)
    b = random.randint(1, 9)

    session["captcha"] = a + b

    return f"{a} + {b}"
=======
from flask import (
    Blueprint, request, jsonify
)

from core.security.captcha import generate_captcha, validate_captcha


captcha_bp = Blueprint("captcha", __name__, url_prefix="/captcha")

# CAPTCHA JWT - gera e retorna JSON com pergunta e token
@captcha_bp.route("", methods=["GET"])
def get_captcha():
    captcha_data = generate_captcha()
    return jsonify(captcha_data)
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)


@captcha_bp.route("/captcha-verify", methods=["POST"])
@login_required
def captcha_verify():
<<<<<<< HEAD

    resposta = request.form.get("resposta")

    if not resposta or not resposta.isdigit():
        return "resposta_invalida", 400

    if int(resposta) == session.get("captcha"):
        return redirect(url_for("dashboard"))
=======
    try:
        data = request.get_json(silent=True) or request.form

        # Pega o token do captcha (não csrf_token!)
        token = data.get("captcha_token")
        answer = data.get("captcha_answer")

        if not token or answer is None:
            return jsonify({"status": "captcha_invalido"}), 400

        if validate_captcha(token, answer):
            return jsonify({"status": "captcha_correto"}), 200
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)

    return "captcha_incorreto", 401
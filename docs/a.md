import secrets
from datetime import datetime, timezone, timedelta

from flask import (
    Blueprint, request, redirect,
    session, render_template, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

from core.db.connection import get_connection
from core.db.tenant import get_tenant_connection
from core.extensions import limiter, MAX_TENTATIVAS, BLOQUEIO_MINUTOS

# Cria o blueprint
auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")

        if not email or not senha or not confirmar_senha:
            return "erro_campos_vazios", 401
        if len(email) > 254:
            return "erro_email_invalido", 401
        if len(senha) < 8:
            return "senha_muito_curta", 400
        if senha != confirmar_senha:
            return "erro_confirmacao_senha", 400

        senha_hash = generate_password_hash(senha)
        conn = get_connection("primeza_db")
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO users
                (email, password, created_at, failed_attempts, locked_until)
                VALUES (%s,%s,%s,0,NULL)
            """, (email, senha_hash, datetime.now(timezone.utc)))
            conn.commit()
        except Exception as e:
            conn.rollback()
            if hasattr(e, 'pgcode') and e.pgcode == '23505':  # UniqueViolation
                return "usuario_ja_existe", 400
            return "erro_interno_register", 500
        finally:
            cur.close()
            conn.close()

        return redirect(url_for("auth.login"))

    return render_template("auth/cadastro.html")


# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("30 per minute")
def login():
    show_captcha = False

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha")

        captcha_token = request.form.get("captcha_token")
        captcha_answer = request.form.get("captcha_answer")

        if not email or not senha:
            return render_template("auth/login.html", show_captcha=False)

        conn = get_connection("primeza_db")
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("""
                SELECT id, password, failed_attempts, locked_until
                FROM users
                WHERE email = %s
            """, (email,))
            user = cur.fetchone()

            if not user:
                return render_template("auth/login.html", show_captcha=False)

            user_id = user["id"]
            password_hash = user["password"]
            failed_attempts = user["failed_attempts"]
            locked_until = user["locked_until"]

            # conta bloqueada
            if locked_until and datetime.now(timezone.utc) < locked_until:
                return render_template("auth/login.html", show_captcha=True, error="conta_bloqueada")

            # ativa captcha
            if failed_attempts >= 3:
                show_captcha = True

                from core.security.captcha import validate_captcha

                if not captcha_token or not captcha_answer:
                    return render_template("auth/login.html", show_captcha=True)

                if not validate_captcha(captcha_token, captcha_answer, request.remote_addr):
                    return render_template("auth/login.html", show_captcha=True, error="captcha_invalido")

            # senha correta
            if check_password_hash(password_hash, senha):
                token = secrets.token_hex(64)

                cur.execute("""
                    UPDATE users
                    SET failed_attempts = 0,
                        locked_until = NULL,
                        last_login = %s,
                        user_token = %s
                    WHERE id = %s
                """, (datetime.now(timezone.utc), token, user_id))

                conn.commit()

                session.clear()
                session["auth"] = True
                session["user_id"] = user_id

                return redirect(url_for("system.index"))

            # senha errada
            failed_attempts += 1

            cur.execute("""
                UPDATE users
                SET failed_attempts = %s
                WHERE id = %s
            """, (failed_attempts, user_id))

            conn.commit()

            return render_template(
                "auth/login.html",
                show_captcha=(failed_attempts >= 3),
                error="login_invalido"
            )

        except Exception as e:
            conn.rollback()
            print(e)
            return render_template("auth/login.html", show_captcha=False)

        finally:
            cur.close()
            conn.close()

    # 🔹 GET
    if session.get("auth"):
        return redirect(url_for("system.index"))

    return render_template("auth/login.html", show_captcha=False)

# LOGOUT
@auth_bp.route("/logout", methods=["POST"])
def logout():
    conn = get_tenant_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE users
            SET user_token = NULL
            WHERE id = %s
        """, (session.get("user_id"),))
        conn.commit()
    except:
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    session.clear()
    return redirect(url_for("auth.login"))






Para amanhã, não esquecer:
1. Login sempre acontece no backend
2. Backend decide se captcha é obrigatório
3. Se for obrigatório:
    - sem captcha → bloqueia
    - captcha inválido → bloqueia
4. Se não for:
    - ignora captcha completamente
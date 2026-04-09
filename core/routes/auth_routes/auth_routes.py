import secrets
from datetime import datetime, timezone, timedelta

from flask import Blueprint, request, redirect, session, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

from core.db.connection import get_connection
from core.extensions import limiter, MAX_TENTATIVAS, BLOQUEIO_MINUTOS

# captcha
from core.security.captcha import validate_captcha, consume_captcha

# Cria o blueprint
auth_bp = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================
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
            if hasattr(e, 'pgcode') and e.pgcode == '23505':
                return "usuario_ja_existe", 400
            return "erro_interno_register", 500
        finally:
            cur.close()
            conn.close()

        return redirect(url_for("auth.login"))

    return render_template("auth/cadastro.html")


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("30 per minute")
def login():
    show_captcha = False

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha")

        if not email or not senha:
<<<<<<< HEAD
            return "login_invalido", 401
=======
            return render_template("auth/login.html", show_captcha=False)
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)

        conn = get_connection("primeza_db")
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("""
                SELECT id,password,failed_attempts,locked_until
                FROM users
                WHERE email = %s
            """, (email,))
            user = cur.fetchone()

            if not user:
<<<<<<< HEAD
                return "login_invalido", 401
=======
                return render_template("auth/login.html", show_captcha=False)
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)

            user_id = user["id"]
            password_hash = user["password"]
            failed_attempts = user["failed_attempts"]
            locked_until = user["locked_until"]

<<<<<<< HEAD
            if locked_until and datetime.now(timezone.utc) < locked_until:
                return "conta_bloqueada", 403

=======
            # =========================
            # BLOQUEIO
            # =========================
            if locked_until and datetime.now(timezone.utc) < locked_until:
                return render_template(
                    "auth/login.html",
                    show_captcha=True,
                    error="conta_bloqueada"
                )

            # =========================
            # CAPTCHA (APÓS 3 TENTATIVAS)
            # =========================
            if failed_attempts >= 3:

                # exige presença dos dados do captcha
                if not captcha_token or not captcha_answer:
                    return render_template(
                        "auth/login.html",
                        show_captcha=True,
                        error="captcha_obrigatorio"
                    )

                # valida captcha amarrado ao contexto da requisição (IP)
                if not validate_captcha(captcha_token, captcha_answer):
                    return render_template(
                        "auth/login.html",
                        show_captcha=True,
                        error="captcha_invalido"
                    )

            # =========================
            # SENHA CORRETA
            # =========================
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)
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
                session["tenant_db"] = "primeza_db"  # Set tenant database for user operations

                # Marca captcha como consumido (se foi usado)
                if captcha_token:
                    consume_captcha(captcha_token)

                return redirect(url_for("system.index"))

<<<<<<< HEAD
            failed_attempts += 1
            if failed_attempts >= 3:
                return redirect(url_for("captcha.captcha"))

            if failed_attempts >= MAX_TENTATIVAS:
                lock_time = datetime.now(timezone.utc) + timedelta(minutes=BLOQUEIO_MINUTOS)
=======
            # =========================
            # SENHA ERRADA
            # =========================
            failed_attempts += 1

            # Bloqueia após 5 tentativas
            if failed_attempts >= 5:
                bloqueio_ate = datetime.now(timezone.utc) + timedelta(minutes=15)
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)
                cur.execute("""
                    UPDATE users
                    SET failed_attempts = %s,
                        locked_until = %s
                    WHERE id = %s
<<<<<<< HEAD
                """, (lock_time, user_id))
=======
                """, (failed_attempts, bloqueio_ate, user_id))
                conn.commit()
                return render_template(
                    "auth/login.html",
                    show_captcha=False,
                    error="conta_bloqueada_tentativas"
                )
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)
            else:
                cur.execute("""
                    UPDATE users
                    SET failed_attempts = %s
                    WHERE id = %s
                """, (failed_attempts, user_id))
<<<<<<< HEAD

            conn.commit()
            return "login_invalido", 401

        except Exception as e:
            conn.rollback()
            print("Erro:", e)
            return "erro_interno_login", 500
=======
                conn.commit()

            return render_template(
                "auth/login.html",
                show_captcha=(failed_attempts >= 3),
                error="login_invalido"
            )

        except Exception as e:
            conn.rollback()
            print("Erro login:", e)
            return render_template("auth/login.html", show_captcha=False)
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)

        finally:
            cur.close()
            conn.close()

    # =========================
    # GET
    # =========================
    if session.get("auth"):
        return redirect(url_for("system.index"))

    return render_template("auth/login.html", show_captcha=False)


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    user_id = session.get("user_id")
    
    if user_id:
        conn = get_connection("primeza_db")
        cur = conn.cursor()

        try:
            cur.execute("""
                UPDATE users
                SET user_token = NULL
                WHERE id = %s
            """, (user_id,))
            conn.commit()
        except:
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    session.clear()
    return redirect(url_for("auth.login"))
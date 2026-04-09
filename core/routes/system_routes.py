from flask import (
    render_template, request,
    jsonify, session,
    url_for, redirect,
    Blueprint
)

from core.db.connection import get_connection
from core.security.security import login_required


system_bp = Blueprint("system", __name__)
<<<<<<< HEAD
=======
captcha_bp = Blueprint("captcha", __name__, url_prefix="/captcha")

>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)

# ROTAS PÚBLICAS
@system_bp.route("/")
@system_bp.route("/atria")
def atria():
    return render_template("landing_page/atria.html")


# ROTAS PRIVADAS
@system_bp.route("/index")
@login_required
def index():
<<<<<<< HEAD
    return render_template("sistema/index.html")
=======
    return render_template("sistema/index.html")   


@captcha_bp.route("/", methods=["GET"])
def get_captcha():
    captcha_data = generate_captcha()
    return jsonify(captcha_data)
>>>>>>> 5833c60 (feat(security, auth, payment): implementei captcha inteligente + fortaleci autenticação + iniciei integração de pagamentos)


@system_bp.route("/sobre")
@login_required
def sobre():
    return render_template("sistema/sobre.html")


@system_bp.route("/index_page")
@login_required
def index_page():
    return render_template("sistema/index_page.html")


@system_bp.route("/contato")
@login_required
def contato():
    return render_template("sistema/contato.html")


@system_bp.route("/form")
@login_required
def form():
    return render_template("sistema/form.html")


@system_bp.route("/produto_01")
@login_required
def produto_01():
    return render_template("sistema/produto_01.html")


@system_bp.route("/produto_02")
@login_required
def produto_02():
    return render_template("sistema/produto_02.html")


@system_bp.route("/produto_03")
@login_required
def produto_03():
    return render_template("sistema/produto_03.html")


@system_bp.route("/produto_04")
@login_required
def produto_04():
    return render_template("sistema/produto_04.html")


@system_bp.route("/sucesso")
@login_required
def sucesso():
    return render_template("sistema/sucesso.html")


@system_bp.route("/dashboard")
@login_required
def dashboard():
    return "Área protegida"


# SALVAR CLIENTE
@system_bp.route("/salvar_cliente", methods=["POST"])
@login_required
def salvar_cliente():

    tenant_db = session.get("tenant_db")
    
    if not tenant_db:
        return jsonify({
            "status": "erro",
            "mensagem": "Sessão inválida. Faça login novamente."
        }), 401

    dados = {
        "nome": request.form.get("nome") or "",
        "email": request.form.get("email") or "",
        "ddi": request.form.get("ddi") or "",
        "ddd": request.form.get("ddd") or "",
        "telefone": request.form.get("telefone") or "",
        "endereco": request.form.get("endereco") or "",
        "numero": request.form.get("numero") or "",
        "bairro": request.form.get("bairro") or "",
        "complemento": request.form.get("complemento") or "",
        "cidade": request.form.get("cidade") or "",
        "estado": request.form.get("estado") or "",
        "cep": request.form.get("cep") or "",
        "pais": request.form.get("pais") or ""
    }

    def only_digits(v):
        return "".join(filter(str.isdigit, v))

    dados["ddi"] = only_digits(dados["ddi"])
    dados["ddd"] = only_digits(dados["ddd"])
    dados["telefone"] = only_digits(dados["telefone"])
    dados["cep"] = only_digits(dados["cep"])

    obrigatorios = [
        "nome","email","telefone","endereco",
        "numero","bairro","cidade","estado","cep"
    ]

    for campo in obrigatorios:
        if not dados[campo]:
            return jsonify({
                "status":"erro",
                "mensagem": f"Campo obrigatório {campo} está vazio"
            }), 400

    conn = None
    try:
        conn = get_connection(tenant_db)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO "endereço_completo"
            (nome, email, ddi, ddd, telefone, endereco, numero, bairro, complemento, cidade, estado, cep, pais)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            dados["nome"], dados["email"], dados["ddi"], dados["ddd"], dados["telefone"],
            dados["endereco"], dados["numero"], dados["bairro"], dados["complemento"],
            dados["cidade"], dados["estado"], dados["cep"], dados["pais"]
        ))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"[ERRO salvar_cliente] {e}")
        if conn: conn.rollback()
        return jsonify({"status":"erro","mensagem":str(e)}), 500
    finally:
        if conn: conn.close()

    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status":"sucesso","mensagem":"Cliente criado com sucesso"})
    else:
        return redirect(url_for("system.sucesso"))
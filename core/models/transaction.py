from flask import (
    render_template,
    session, jsonify,
    request, Blueprint
)
from core.security.security import login_required

transaction_bp = Blueprint('transaction', __name__)

def criar_transacao(conn, transacao):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transacoes (
            transacao_id, cliente_id, produto_id, valor, status
        ) VALUES (%s, %s, %s, %s, %s)
    """, (
        transacao["transacao_id"],
        transacao["cliente_id"],
        transacao["produto_id"],
        transacao["valor"],
        transacao["status"]
    ))

    conn.commit()
    cur.close()


def atualizar_transacao(conn, transacao_id, dados):
    cur = conn.cursor()

    cur.execute("""
        UPDATE transacoes
        SET status = %s,
            gateway_id = %s,
            mensagem = %s,
            atualizado_em = NOW()
        WHERE transacao_id = %s
    """, (
        dados["status"],
        dados["gateway_id"],
        dados["mensagem"],
        transacao_id
    ))

    conn.commit()
    cur.close()


# PAYMENT ROUTE
@transaction_bp.route("/v1/payments", methods=["POST"])
@login_required
def criar_pagamento():
    from core.services.payment_service import process_payment  # Lazy import
    
    dados = request.get_json()
    resultado = process_payment(
        user_id=session.get("user_id"),
        dados=dados
    )
    return jsonify(resultado)
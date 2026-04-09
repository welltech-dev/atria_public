import uuid
import requests

from flask import session


from core.db.connection import get_connection
from core.config.config import GATEWAY_URL


# PAYMENT (mantido interno, removida duplicidade de import)
def process_payment(user_id, dados):

    produto_id = dados.get("produto_id")

    if not produto_id:
        return {"erro": "produto_id obrigatório"}, 400

    try:
        conn = get_connection(session.get("tenant_db"))
        cur = conn.cursor()

        cur.execute("SELECT valor FROM produtos WHERE id = %s", (produto_id,))
        result = cur.fetchone()

        cur.close()
        conn.close()

    except Exception:
        return {"erro": "erro ao buscar produto"}, 500

    if not result:
        return {"erro": "produto não encontrado"}, 404

    valor = result[0]

    transacao_id = str(uuid.uuid4())

    payload = {
        "transacao_id": transacao_id,
        "valor": valor,
        "cliente_id": user_id
    }

    if not GATEWAY_URL:
        return {"erro": "gateway não configurado"}, 500

    try:
        response = requests.post(
            GATEWAY_URL + "/bank/create-checkout",
            json=payload,
            timeout=5
        )
        response.raise_for_status()

    except requests.RequestException:
        return {"erro": "falha no gateway"}, 502

    return {
        "checkout_url": response.json().get("checkout_url"),
        "transacao_id": transacao_id
    }

    produto_id = dados.get("produto_id")

    if not produto_id:
        return {"erro": "produto_id obrigatório"}, 400

    try:
        conn = get_connection(session.get("tenant_db"))
        cur = conn.cursor()

        cur.execute("SELECT valor FROM produtos WHERE id = %s", (produto_id,))
        result = cur.fetchone()

        cur.close()
        conn.close()

    except Exception:
        return {"erro": "erro ao buscar produto"}, 500

    if not result:
        return {"erro": "produto não encontrado"}, 404

    valor = result[0]

    transacao_id = str(uuid.uuid4())

    payload = {
        "transacao_id": transacao_id,
        "valor": valor,
        "cliente_id": user_id
    }

    if not GATEWAY_URL:
        return {"erro": "gateway não configurado"}, 500

    try:
        response = requests.post(
            GATEWAY_URL + "/bank/create-checkout",
            json=payload,
            timeout=5
        )
        response.raise_for_status()

    except requests.RequestException:
        return {"erro": "falha no gateway"}, 502

    return {
        "checkout_url": response.json().get("checkout_url"),
        "transacao_id": transacao_id
    }
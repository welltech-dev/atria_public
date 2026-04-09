import requests

def enviar_pagamento(transacao):

    response = requests.post(
        "http://127.0.0.1:3000/bank/pay",
        json=transacao,
        timeout=5
    )

    data = response.json()

    status_map = {
        "PAID": "aprovado",
        "DECLINED": "recusado",
        "PENDING": "pendente"
    }

    return {
        "status": status_map.get(data.get("bank_code"), "erro"),
        "gateway_id": data.get("bank_id"),
        "mensagem": data.get("message")
    }
async function gatewayPagamento(transacao) {
  // simulação de resposta do banco
  const respostasPossiveis = [
    { code: "PAID", message: "Aprovado!" },
    { code: "DECLINED", message: "Cancelado." },
    { code: "PENDING", message: "Em Análise." }
  ];

  const sorteio = Math.floor(Math.random() * respostasPossiveis.length);
  return {
    bank_code: respostasPossiveis[sorteio].code,
    bank_message: respostasPossiveis[sorteio].message,
    bank_id: "banco_XXXXXX" + Date.now()
  };
}

module.exports = gatewayPagamento;

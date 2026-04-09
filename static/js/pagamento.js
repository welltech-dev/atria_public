document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formPagamento");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const produto_id = form.querySelector('input[name="produto_id"]').value;
        const csrf_token = form.querySelector('input[name="csrf_token"]').value;

        try {
            const response = await fetch("/v1/payments", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ 
                    produto_id,
                    csrf_token 
                })
            });

            const data = await response.json();

            if (response.ok) {
                // redireciona para checkout ou mostra link
                window.location.href = data.checkout_url;
            } else {
                alert(data.erro || "Erro ao processar pagamento");
            }
        } catch (err) {
            console.error(err);
            alert("Erro de conexão com o servidor");
        }
    });
});
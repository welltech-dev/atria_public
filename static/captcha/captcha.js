document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("captcha-modal");
    if (!modal) return;

    const questionEl = document.getElementById("captcha-question");
    const answerEl = document.getElementById("captcha-answer");
    const submitBtn = document.getElementById("captcha-submit");
    const feedbackEl = document.getElementById("captcha-feedback");

    const hiddenToken = document.getElementById("captcha-token");
    const hiddenAnswer = document.getElementById("captcha-answer-hidden");

    let captchaToken = "";
    let isSubmitting = false;

    // estado global controlado
    window.captchaValidated = false;

    function showModal() {
        modal.classList.remove("hidden");
    }

    function hideModal() {
        modal.classList.add("hidden");
    }

    async function loadCaptcha() {
        try {
            const res = await fetch("/captcha/");
            const data = await res.json();

            if (data.question && data.token) {
                questionEl.textContent = data.question;
                captchaToken = data.token;

                // reset estado
                window.captchaValidated = false;
                answerEl.value = "";
                feedbackEl.textContent = "";

                showModal();
            }

        } catch (err) {
            console.error("Erro ao carregar captcha:", err);
        }
    }

    async function submitCaptcha(e) {
        if (e) e.preventDefault();

        if (isSubmitting) {
            console.log("Submissão já em andamento, ignorando novo clique");
            return;
        }

        isSubmitting = true;
        submitBtn.disabled = true;
        feedbackEl.textContent = "Verificando...";

        const answer = answerEl.value.trim();

        if (!answer) {
            feedbackEl.textContent = "Digite a resposta";
            isSubmitting = false;
            submitBtn.disabled = false;
            return;
        }

        // Debug: log da resposta que será enviada
        console.log("Enviando resposta:", { 
            token: captchaToken?.substring(0, 20) + "...", 
            answer: answer 
        });

        try {
            const formData = new FormData();
            formData.append("captcha_token", captchaToken);
            formData.append("captcha_answer", answer);

            const res = await fetch("/captcha/verify", {
                method: "POST",
                body: formData
            });

            const json = await res.json();
            console.log("Resposta do servidor:", json, "Status:", res.status);

            if (res.ok) {
                // ✅ Sucesso - amarra no form de login
                if (hiddenToken && hiddenAnswer) {
                    hiddenToken.value = captchaToken;
                    hiddenAnswer.value = answer;
                }

                window.captchaValidated = true;
                feedbackEl.textContent = "Captcha correto!";
                answerEl.disabled = true;
                submitBtn.disabled = true;
                
                // Aguarda um pouco antes de fechar
                setTimeout(() => {
                    hideModal();
                    // Reset para próxima vez
                    setTimeout(() => {
                        answerEl.disabled = false;
                        submitBtn.disabled = false;
                        isSubmitting = false;
                    }, 500);
                }, 500);

            } else {
                // ❌ Erro - carrega novo captcha
                feedbackEl.textContent = "Resposta incorreta. Tente novamente.";
                answerEl.value = "";
                window.captchaValidated = false;
                submitBtn.disabled = false;
                isSubmitting = false;

                // Carrega novo captcha
                setTimeout(() => loadCaptcha(), 800);
            }

        } catch (err) {
            console.error("Erro ao validar captcha:", err);
            feedbackEl.textContent = "Erro na conexão. Tente novamente.";
            window.captchaValidated = false;
            submitBtn.disabled = false;
            isSubmitting = false;
        }
    }

    // Remove listeners anteriores e adiciona apenas um
    if (submitBtn) {
        // Remove todos os listeners antigos (se houver)
        const newBtn = submitBtn.cloneNode(true);
        submitBtn.parentNode.replaceChild(newBtn, submitBtn);
        
        // Adiciona listener novo
        const currentSubmitBtn = document.getElementById("captcha-submit");
        if (currentSubmitBtn) {
            currentSubmitBtn.addEventListener("click", submitCaptcha);
            // Também suporta Enter no input
            answerEl.addEventListener("keypress", (e) => {
                if (e.key === "Enter") {
                    submitCaptcha(e);
                }
            });
        }
    }

    // ponto de entrada controlado pelo backend
    if (window.showCaptcha === true) {
        loadCaptcha();
    }

});
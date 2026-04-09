document.addEventListener("DOMContentLoaded", () => {
  const paisInput = document.querySelector("#paisTelefone");
  const telefoneInput = document.querySelector("#telefoneCompleto");
  const ddiInput = document.querySelector("#ddi");
  const dddInput = document.querySelector("ddd");
  const telLocalInput = document.querySelector("#telefone_local");

  if (!paisInput || !telefoneInput || !ddiInput || !dddInput || !telLocalInput) return;

  // Inicializa o intl-tel-input só para DDI com bandeira
  const iti = window.intlTelInput(paisInput, {
    initialCountry: "br",
    separateDialCode: true,
    nationalMode: false, // não interfere, só DDI
    utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/18.2.1/js/utils.js",
  });

  // Atualiza DDI quando trocar país
  const atualizarDDI = () => {
    const data = iti.getSelectedCountryData();
    ddiInput.value = data.dialCode;
    paisInput.value = `+${data.dialCode}`;
  };

  atualizarDDI();
  paisInput.addEventListener("countrychange", atualizarDDI);

  // Antes de enviar o formulário
  const form = telefoneInput.closest("form");
  if (!form) return;

  form.addEventListener("submit", () => {
    const telefoneRaw = telefoneInput.value.replace(/\D/g, ""); // só números
    if (!telefoneRaw) return;

    // separa DDD (2 primeiros dígitos) + telefone
    dddInput.value = telefoneRaw.slice(0, 2);
    telLocalInput.value = telefoneRaw.slice(2);
  });
});

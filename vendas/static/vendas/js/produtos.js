document.addEventListener("DOMContentLoaded", function () {
  var botoes = document.querySelectorAll(".step-btn");

  botoes.forEach(function (botao) {
    botao.addEventListener("click", function () {
      var idAlvo = botao.getAttribute("data-alvo");
      var input = document.getElementById(idAlvo);
      var valorAtual = parseInt(input.value, 10) || 0;

      if (botao.classList.contains("step-mais")) {
        if (valorAtual < 50) {
          input.value = valorAtual + 1;
        }
      } else {
        if (valorAtual > 0) {
          input.value = valorAtual - 1;
        }
      }
    });
  });
});
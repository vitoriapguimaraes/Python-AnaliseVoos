// Efeitos hover simplificados
document.addEventListener("DOMContentLoaded", function () {
  addHoverEffects();
});

function addHoverEffects() {
  // Efeito hover para os cards
  const cards = document.querySelectorAll(".big-number-card");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-5px)";
      this.style.boxShadow = "0 8px 15px rgba(0,0,0,0.2)";
    });
    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
      this.style.boxShadow = "0 4px 6px rgba(0,0,0,0.1)";
    });
  });
}

function setupMetricButtons() {
  // Configuração dos botões de métrica
  const buttons = document.querySelectorAll(".metric-button");
  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      // Remove classe active de todos os botões
      buttons.forEach((btn) => btn.classList.remove("active"));
      // Adiciona classe active ao botão clicado
      this.classList.add("active");

      // Dispara evento para o Dash
      const metricValue = this.getAttribute("data-value");
      if (window.dash_clientside && window.dash_clientside.setMetric) {
        window.dash_clientside.setMetric(metricValue);
      }
    });
  });

  // Ativa o primeiro botão por padrão
  if (buttons.length > 0) {
    buttons[0].classList.add("active");
  }
}

// Função global para o Dash acessar
window.dash_clientside = Object.assign({}, window.dash_clientside, {
  setMetric: function (value) {
    return value;
  },
});

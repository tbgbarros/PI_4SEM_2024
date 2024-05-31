
document.addEventListener("DOMContentLoaded", function () {
    let contador = 60;
    const contadorElement = document.getElementById('contador');
    const umTerco = 20;
    const doisTercos = 40;

    const intervalo = setInterval(() => {
        contador--;

        if (contador > doisTercos) {
            contadorElement.style.color = 'green';
        } else if (contador > umTerco) {
            contadorElement.style.color = 'yellow';
        } else {
            contadorElement.style.color = 'red';
        }

        contadorElement.textContent = contador;

        if (contador <= 0) {
            clearInterval(intervalo);
            bloquearInteracao();
        }
    }, 1000);

    function bloquearInteracao() {
        document.body.innerHTML += '<div id="bloqueio" class="red"><h1>Tempo Esgotado</h1></div>';
        setTimeout(() => {
            window.location.href = "/";
        }, 3000); // 3 segundos
    }
});

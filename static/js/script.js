/* =========================================
   VARIABLES GLOBALES
   (Deben estar afuera para que todos las vean)
   ========================================= */
let lastResult = null; // Aquí se guardarán los datos de la predicción
let myChart = null;    // Aquí vive el gráfico

/* =========================================
   FUNCIÓN 1: RENDERIZAR GRÁFICO
   ========================================= */
function renderChart(percentage) {
    const ctx = document.getElementById('riskChart').getContext('2d');
    const remaining = 100 - percentage;
    
    // Colores dinámicos
    let color = '#198754'; // Verde
    if (percentage > 50) color = '#dc3545';      // Rojo
    else if (percentage > 25) color = '#ffc107'; // Amarillo

    // Limpiar gráfico anterior si existe
    if (myChart) {
        myChart.destroy();
    }

    // Crear nuevo gráfico
    myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Riesgo', 'Retención'],
            datasets: [{
                data: [percentage, remaining],
                backgroundColor: [color, '#f8f9fa'],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, 
            cutout: '75%', 
            plugins: {
                legend: { display: false }, 
                tooltip: { enabled: true }
            }
        }
    });
}

/* =========================================
   FUNCIÓN 2: DESCARGAR PDF
   ========================================= */
function downloadPDF() {
    console.log("Intentando descargar PDF..."); // Para depuración
    console.log("Datos guardados:", lastResult); // Ver si está vacío en consola

    // Validación de seguridad
    if(!lastResult) {
        alert("Primero debes realizar un análisis para generar el reporte.");
        return;
    }
    
    // Petición al servidor
    fetch('/download_report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            risk: lastResult.risk,
            prob: lastResult.probability,
            advice: lastResult.advice
        })
    })
    .then(resp => {
        if (!resp.ok) throw new Error("Error generando PDF");
        return resp.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'Dictamen_ESCOM.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(err => {
        console.error(err);
        alert("No se pudo descargar el PDF. Revisa la consola.");
    });
}

/* =========================================
   INICIALIZACIÓN Y EVENTOS
   ========================================= */
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Configurar Botón PDF
    const btnPdf = document.getElementById('btnPdf');
    if (btnPdf) {
        btnPdf.addEventListener('click', downloadPDF);
    }

    // 2. Configurar Formulario de Predicción
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault(); 
    
            // UI: Cambiar a modo "Procesando"
            document.getElementById('state-waiting').style.display = 'none';
            const resultPanel = document.getElementById('state-result');
            resultPanel.style.display = 'block';
            resultPanel.classList.add('fade-in'); 
    
            document.getElementById('percentageText').innerText = "--";
            const riskLabel = document.getElementById('riskLabel');
            riskLabel.innerText = "PROCESANDO...";
            riskLabel.className = "badge rounded-pill bg-secondary px-3 py-2";
    
            // Recolectar datos
            const data = {
                semestre: document.getElementById('semestre').value,
                turno: document.getElementById('turno').value,
                debtor: document.getElementById('debtor').value,
                promedio_general: document.getElementById('promedio_general').value,
                promedio_anterior: document.getElementById('promedio_anterior').value,
                creditos: document.getElementById('creditos').value,
                periodos_restantes: document.getElementById('periodos_restantes').value,
                scholarship: document.getElementById('scholarship').value,
                age: document.getElementById('age').value
            };
    
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
    
                if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
                const result = await response.json();
    
                if (result.error) {
                    alert("Error del Servidor: " + result.error);
                    return;
                }
    
                // --- AQUÍ OCURRE LA MAGIA ---
                // Guardamos el resultado en la variable global
                lastResult = result;
                console.log("Resultado guardado correctamente:", lastResult);
                // -----------------------------
    
                // Actualizar UI con los datos
                document.getElementById('percentageText').innerText = result.probability + "%";
                
                riskLabel.innerText = result.risk;
                if(result.probability > 50) {
                    riskLabel.className = "badge rounded-pill bg-danger px-3 py-2";
                } else if (result.probability > 25) {
                    riskLabel.className = "badge rounded-pill bg-warning text-dark px-3 py-2";
                } else {
                    riskLabel.className = "badge rounded-pill bg-success px-3 py-2";
                }
    
                const list = document.getElementById('adviceList');
                list.innerHTML = ""; 
                result.advice.forEach(item => {
                    let cleanItem = item.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
                    let li = document.createElement('li');
                    li.className = "mb-2";
                    li.innerHTML = `<i class="bi bi-check2-circle text-success me-2"></i>${cleanItem}`;
                    list.appendChild(li);
                });
    
                renderChart(result.probability);
    
            } catch (error) {
                console.error("Error:", error);
                alert("Hubo un error al conectar con el servidor.");
            }
        });
    }
});
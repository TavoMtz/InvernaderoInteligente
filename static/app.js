//Archivos estáticos
// Función principal que atrapa los datos de Flask
function obtenerDatosDelSensor() {
    fetch('/api/sensores')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.warn("Esperando datos del Arduino...", data.error);
                return;
            }

            // Actualizar Temperatura y Humedad
            document.getElementById('temp').innerText = data.temperatura + " °C";
            document.getElementById('hum').innerText = data.humedad + " %";

            // Lógica para el Motor A
            const motorA = document.getElementById('motorA');
            if (data.motorA === 1) {
                motorA.innerText = "Encendido";
                motorA.className = "status-on";
            } else {
                motorA.innerText = "Apagado";
                motorA.className = "status-off";
            }

            // Lógica para el Motor B
            const motorB = document.getElementById('motorB');
            if (data.motorB === 1) {
                motorB.innerText = "Encendido";
                motorB.className = "status-on";
            } else {
                motorB.innerText = "Apagado";
                motorB.className = "status-off";
            }
            // Mostrar la sugerencia de la IA
            if (data.sugerencia_ia) {
                document.getElementById('sugerencia-texto').innerText = data.sugerencia_ia;
            }
        })
        .catch(error => console.error('Error de conexión con Flask:', error));

}

// Ejecutar al cargar y luego cada 1 segundo
obtenerDatosDelSensor();
setInterval(obtenerDatosDelSensor, 1000);
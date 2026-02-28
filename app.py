from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import serial
import json
import time
import os

load_dotenv()
app = Flask(__name__)

# Configura tu puerto (el que te funcionó, ej. 'COM3')
PUERTO_SERIAL = 'COM5' 

try:
    arduino = serial.Serial(PUERTO_SERIAL, 9600, timeout=1)
    time.sleep(2)
    print(f"Conectado exitosamente al Arduino en el puerto {PUERTO_SERIAL}")
except Exception as e:
    arduino = None
    print(f"Advertencia: No se pudo conectar al Arduino. Error: {e}")

# --- NUEVA FUNCIÓN DE "IA" (Sistema Experto) ---
def generar_recomendacion(temp, hum):
    """
    Evalúa las condiciones actuales basándose en los parámetros biológicos del rábano.
    """
    alertas = []
    
    # Evaluación de Temperatura
    if temp > 25.0:
        alertas.append("⚠️ Temperatura alta para el rábano. Riesgo de estrés térmico.")
    elif temp < 10.0:
        alertas.append("❄️ Temperatura muy baja. El crecimiento del rábano puede detenerse.")
        
    # Evaluación de Humedad
    if hum < 40.0:
        alertas.append("💧 Humedad ambiente baja. Verifica la humedad del suelo pronto.")
    elif hum > 80.0:
        alertas.append("🌧️ Humedad muy alta. Riesgo de aparición de hongos en las hojas.")

    # Si no hay alertas, el sistema reporta un estado óptimo
    if not alertas:
        return "✅ Condiciones óptimas para el ciclo de crecimiento del rábano."
    
    # Unir todas las alertas generadas en un solo texto
    return " | ".join(alertas)


@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/sensores')
def api_sensores():
    if arduino is None:
        return jsonify({"error": "Arduino no conectado"}), 503

    try:
        arduino.reset_input_buffer()
        linea = arduino.readline().decode('utf-8').strip()
        
        if linea:
            datos = json.loads(linea)
            
            # --- INYECTAR LA RECOMENDACIÓN EN LOS DATOS ---
            recomendacion = generar_recomendacion(datos['temperatura'], datos['humedad'])
            datos['sugerencia_ia'] = recomendacion
            
            return jsonify(datos), 200
        else:
            return jsonify({"error": "No se recibieron datos"}), 204

    except json.JSONDecodeError:
        return jsonify({"error": "Error decodificando el JSON."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
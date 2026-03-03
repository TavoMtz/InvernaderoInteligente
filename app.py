from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import serial
import json
import time
import os
import requests  # <-- NUEVA LIBRERIA

load_dotenv()
app = Flask(__name__)

# Configura tu puerto (el que te funciono, ej. 'COM5')
PUERTO_SERIAL = 'COM5' 

# Cargar credenciales de Telegram desde el .env
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Variable global para recordar el ultimo mensaje y evitar spam
ultima_alerta = "" 

try:
    arduino = serial.Serial(PUERTO_SERIAL, 9600, timeout=1)
    time.sleep(2)
    print(f"Conectado exitosamente al Arduino en el puerto {PUERTO_SERIAL}")
except Exception as e:
    arduino = None
    print(f"Advertencia: No se pudo conectar al Arduino. Error: {e}")

# --- NUEVA FUNCION PARA ENVIAR TELEGRAM ---
def enviar_mensaje_telegram(mensaje):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Faltan credenciales de Telegram en el .env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje
    }
    try:
        requests.post(url, json=payload)
        print("Mensaje de Telegram enviado con exito.")
    except Exception as e:
        print(f"Error al enviar Telegram: {e}")

# --- SISTEMA EXPERTO (IA BASICA) ---
def generar_recomendacion(temp, hum):
    global ultima_alerta
    alertas = []
    
    if temp > 25.0:
        alertas.append("Riesgo de estres termico (Alta temp).")
    elif temp < 10.0:
        alertas.append("Temperatura muy baja. Crecimiento detenido.")
        
    if hum < 40.0:
        alertas.append("Humedad baja. Se encendera la bomba.")
    elif hum > 80.0:
        alertas.append("Humedad muy alta. Riesgo de hongos.")

    if not alertas:
        estado_actual = "Condiciones optimas para el rabano."
    else:
        estado_actual = " | ".join(alertas)
    
    # LOGICA ANTI-SPAM: Solo envia mensaje si el estado es diferente al anterior
    if estado_actual != ultima_alerta:
        enviar_mensaje_telegram(f"Actualizacion del Invernadero:\n{estado_actual}")
        ultima_alerta = estado_actual # Actualiza la memoria
        
    return estado_actual


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
            
            # Generar sugerencia y posible alerta a Telegram
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
    # use_reloader=False evita que el puerto COM se bloquee
    app.run(debug=True, port=5000, use_reloader=False)
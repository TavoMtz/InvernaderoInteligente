from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import serial
import json
import time
import os
import requests
import joblib       # Para cargar el cerebro de la IA
import pandas as pd # Para darle los datos en el formato correcto

load_dotenv()
app = Flask(__name__)

PUERTO_SERIAL = 'COM5' 
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

ultima_alerta = "" 

# --- CARGAR EL MODELO ---
try:
    modelo_ia = joblib.load('modelo_rabano.pkl')
    print("Cerebro de IA (modelo_rabano.pkl) cargado con exito.")
except Exception as e:
    modelo_ia = None
    print(f"Error al cargar el modelo de IA: {e}")

try:
    arduino = serial.Serial(PUERTO_SERIAL, 9600, timeout=1)
    time.sleep(2)
    print(f"Conectado exitosamente al Arduino en el puerto {PUERTO_SERIAL}")
except Exception as e:
    arduino = None
    print(f"Advertencia: No se pudo conectar al Arduino. Error: {e}")

def enviar_mensaje_telegram(mensaje):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error al enviar Telegram: {e}")

# --- EL NUEVO CEREBRO PREDICTIVO ---
def generar_recomendacion(temp, hum, hum_suelo):
    global ultima_alerta
    
    if modelo_ia is None:
        return "Error: IA desconectada."
    # En un proyecto mas avanzado, este dia saldria de una base de datos.
    dia_actual = 15 
    # 1. Preparamos los datos exactamente como los estudio la IA
    datos_entrada = pd.DataFrame([[dia_actual, temp, hum, hum_suelo]], 
                                 columns=['dia', 'temperatura', 'humedad_amb', 'humedad_suelo'])
    
    # 2. La IA hace su prediccion matematica
    agua_predicha = modelo_ia.predict(datos_entrada)[0]
    
    # 3. Traducimos el numero a una recomendacion humana
    if agua_predicha > 0:
        estado_actual = f"IA detecta sequia. Se requieren aprox {agua_predicha:.0f} ml de agua."
    else:
        estado_actual = "IA indica humedad optima. No se requiere riego extra."   
    # Logica anti-spam
    if estado_actual != ultima_alerta:
        enviar_mensaje_telegram(f"Analisis Predictivo:\n{estado_actual}")
        ultima_alerta = estado_actual 
        
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
            
            temp = datos.get('temperatura', 0)
            hum = datos.get('humedad', 0)
            hum_suelo = datos.get('humedad_suelo', 0)
            
            # Pasamos los datos al nuevo cerebro predictivo
            recomendacion = generar_recomendacion(temp, hum, hum_suelo)
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
# 🌱 Invernadero Inteligente Predictivo (IoT + Machine Learning)

Este proyecto automatiza el monitoreo y riego de cultivos a través de un ecosistema de Internet de las Cosas (IoT). A diferencia de los sistemas tradicionales basados en temporizadores o reglas estáticas, este invernadero utiliza un modelo de Machine Learning para predecir la cantidad exacta de agua necesaria basándose en las tasas de evaporación en tiempo real.

##  Características Principales

*  **Riego Predictivo (IA):** Utiliza un modelo *Random Forest Regressor* (precisión del 99.8%) para calcular dinámicamente los mililitros de agua requeridos, evitando el estrés hídrico.
*  **Dashboard de Monitoreo Global:** Interfaz web local expuesta a internet mediante un túnel seguro (Ngrok) para visualización de métricas en tiempo real.
*  **Notificaciones Push:** Integración con la API de Telegram para enviar alertas automatizadas sobre riesgos climáticos (sequía, temperaturas extremas, riesgo de hongos).
*  **Control Físico Independiente:** Actuadores que controlan la irrigación (bomba de agua) y la disipación de calor (ventilador) basados en las predicciones del servidor.

## 🛠️ Stack Tecnológico

**Hardware:**
* Arduino Uno
* Sensor de Temperatura y Humedad DHT11
* Sensor Analógico de Humedad de Suelo
* Módulo Puente H L298N
* Bomba de agua sumergible y ventilador DC

**Software:**
* **Backend:** Python 3, Flask
* **Machine Learning:** Scikit-Learn, Pandas, Joblib
* **Comunicación y Redes:** PySerial, Ngrok, API de Telegram
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TavoMtz/invernadero-inteligente.git](https://github.com/TavoMtz/invernadero-inteligente.git)
cd invernadero-inteligente

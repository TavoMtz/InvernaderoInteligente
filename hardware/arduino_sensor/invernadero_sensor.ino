#include <DHT.h>

#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Pines del puente H
int IN1 = 6;
int IN2 = 5;
int ENA = 3;

int IN3 = 4;
int IN4 = 7;
int ENB = 2;

// Límites para activar los actuadores
float limiteTemp = 30;
float limiteHum = 40;

void setup() {
  Serial.begin(9600);
  dht.begin();

  // Configuración de pines como salida
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Dejar dirección de giro fija para los motores
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void loop() {
  // Lectura del sensor DHT11
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  // Variables para rastrear el estado de los motores (1 = encendido, 0 = apagado)
  int estadoMotorA = 0;
  int estadoMotorB = 0;

  // Lógica del Motor A (Controlado por temperatura)
  if(temp >= limiteTemp) {
    digitalWrite(ENA, HIGH);
    estadoMotorA = 1;
  } else {
    digitalWrite(ENA, LOW);
  }

  // Lógica del Motor B (Controlado por humedad)
  if(hum >= limiteHum) {
    digitalWrite(ENB, HIGH);
    estadoMotorB = 1;
  } else {
    digitalWrite(ENB, LOW);
  }

  // ---------------------------------------------------------
  // SALIDA DE DATOS EN FORMATO JSON
  // ---------------------------------------------------------
  Serial.print("{\"temperatura\": ");
  Serial.print(temp);
  Serial.print(", \"humedad\": ");
  Serial.print(hum);
  Serial.print(", \"motorA\": ");
  Serial.print(estadoMotorA);
  Serial.print(", \"motorB\": ");
  Serial.print(estadoMotorB);
  Serial.println("}");

  // Esperar 1 segundo antes de la siguiente lectura
  delay(1000); 
}
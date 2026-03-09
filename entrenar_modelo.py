import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

def entrenar():
    print("Cargando el dataset sintetico...")
    # 1. Cargar los datos
    df = pd.read_csv('datos_rabano.csv')

    # 2. Separar las variables de entrada (X) de la salida esperada (y)
    X = df[['dia', 'temperatura', 'humedad_amb', 'humedad_suelo']]
    y = df['agua_ml']

    # 3. Dividir los datos: 80% para estudiar, 20% para examen sorpresa
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Crear y entrenar el modelo matematico
    print("Entrenando la Inteligencia Artificial (Random Forest)...")
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # 5. Evaluar que tan bien aprendio con el examen sorpresa
    precision = modelo.score(X_test, y_test)
    print(f"Precision del modelo: {precision * 100:.2f}%")

    # 6. Guardar el modelo empaquetado para usarlo en Flask
    joblib.dump(modelo, 'modelo_rabano.pkl')
    print("Modelo guardado con exito como 'modelo_rabano.pkl'.")

if __name__ == '__main__':
    entrenar()
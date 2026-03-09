import pandas as pd
import random

def generar_dataset(num_filas=1500):
    datos = []
    
    for _ in range(num_filas):
        # Simulamos los 30 dias de crecimiento del rabano
        dia = random.randint(1, 30)
        
        # Simulamos lecturas de tus sensores
        temp = round(random.uniform(10.0, 35.0), 1)
        hum_amb = round(random.uniform(30.0, 90.0), 1)
        hum_suelo = random.randint(150, 600) # 150 = inundado, 600 = desierto
        
        # LOGICA MATEMATICA (Lo que la IA debera aprender a deducir sola)
        agua_ml = 0
        
        # Si el suelo esta seco (mayor a 400), empezamos a calcular el agua
        if hum_suelo > 400:
            agua_ml = (hum_suelo - 400) * 1.5  # Riego base
            
            # Tasa de evaporacion: Si hace calor, necesita mas agua
            if temp > 25:
                agua_ml += 40 
                
        # Etapa de crecimiento: Del dia 15 al 30 el rabano engrosa el bulbo y pide mas agua
        if dia > 15 and agua_ml > 0:
            agua_ml += 35
            
        datos.append([dia, temp, hum_amb, hum_suelo, round(agua_ml)])

    # Convertimos la lista en una tabla estructurada (DataFrame)
    df = pd.DataFrame(datos, columns=['dia', 'temperatura', 'humedad_amb', 'humedad_suelo', 'agua_ml'])
    
    # Guardamos la tabla en un archivo Excel/CSV
    df.to_csv('datos_rabano.csv', index=False)
    print("Archivo 'datos_rabano.csv' generado con exito. Tiene 1500 ejemplos de entrenamiento.")

if __name__ == '__main__':
    generar_dataset()
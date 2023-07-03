import os
import pickle
import pandas as pd
import numpy as np

#Veo en que directorio estoy parada
current_dir = os.getcwd()
print("Directorio de trabajo actual:", current_dir)

# Cargo los datos para el entrenamiento
datos_entrenamiento = pd.read_csv("flaskapp/test/4_datos_test_posttrain.csv")

# Cargo los modelos entrenados
ruta_modelos = 'flaskapp/modelo/dt'
modelos = []
for archivo in os.listdir(ruta_modelos):
    if archivo.endswith(".sav"):
        with open(os.path.join(ruta_modelos, archivo), "rb") as f:
            modelo = pickle.load(f)
            modelos.append(modelo)

# Creo un conjunto de prueba
datos_prueba = datos_entrenamiento.sample(n=15)  #podemos ajustar el tamaño 
# Realizo predicciones con cada modelo
predicciones = []
for modelo in modelos:
    predicciones_modelo = modelo.predict(datos_prueba)  # Realiza las predicciones en los datos de prueba
    predicciones.append(predicciones_modelo)

# Imprimo las predicciones
for i, modelo in enumerate(modelos):
    print(f"Modelo {i+1}:")
    print(predicciones[i])
    print()

expected_predictions = np.array([1] * len(datos_prueba))

for i, model in enumerate(modelos):
    print(f"Model {i+1}:")
    print(predicciones[i])
    assert np.array_equal(predicciones[i], expected_predictions), "CUIDADO: Las predicciones no son las esperadas"
    print("BRAVO: Las predicciones son las esperadas")
    print()



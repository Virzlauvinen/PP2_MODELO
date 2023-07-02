import time

# Definir la función que realiza el entrenamiento del modelo
def entrenar_modelo():
    # Aquí iría el código para entrenar el modelo
    # ...
    # Simulación de tiempo de entrenamiento
    time.sleep(5)  # Espera de 5 segundos para simular el entrenamiento

# Obtener el tiempo de inicio
tiempo_inicio = time.time()

# Llamar a la función de entrenamiento
entrenar_modelo()

# Obtener el tiempo de finalización
tiempo_fin = time.time()

# Calcular el tiempo transcurrido
tiempo_transcurrido = tiempo_fin - tiempo_inicio

# Especificar el tiempo esperado de entrenamiento
tiempo_esperado = 5  # Tiempo esperado en segundos

# Comparar el tiempo real con el tiempo esperado utilizando una aserción
assert tiempo_transcurrido >= tiempo_esperado, "El tiempo de entrenamiento es menor al tiempo esperado"

# Si la aserción no falla, significa que el tiempo de entrenamiento es igual o mayor al tiempo esperado
print("El tiempo de entrenamiento es válido")
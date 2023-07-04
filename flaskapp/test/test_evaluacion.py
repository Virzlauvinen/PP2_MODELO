# import sys
# # sys.path.append('../src')
# from pathlib import Path
# import os
# sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))
# directorio_actual = os.getcwd()
# print("Directorio actual:", directorio_actual)

# from flaskapp.src.modelo_entrenamiento import *
# from src.modelo_entrenamiento import *
# from modelo_entrenamiento import *

#########################################################################################################################

#           NO PUEDO IMPORTAR LAS FUNCIONES DEL MODULO SRC.
#           REALICE TODAS LAS FORMAS POSIBLES DE IMPORTAR Y TODAS DAN ERROR, QUE NO ENCUENTRA EL MODULO.
#           MODIFIEQUE LA RUTA, CAMBIE LOS DIRECTORIOS, AGREGUE LOS __init__.py AL DIRECTORIO.
#           FORCE LA RUTA. CAMBIE LOS DIRECTORIOS DE EJECUCION.

# NADA FUNCIONO. OPTO POR ESCRIBIR TODA LA FUNCION EN ESE ARCHIVO PARA PODER REALIZAR LA PRUEBA DE EVALUACION 

#########################################################################################################################


import time
import pandas as pd
# FUNCION DE LECTURA CSV

def leer_csv(ruta_archivo_csv):
    url = str(ruta_archivo_csv)
    dataset_crudo = pd.read_csv(url)
    return dataset_crudo

# FUNCION DE CLEANING

def data_cleaning(dataset_crudo):
    ''' TOMA UN DATASET Y LO LIMPIA Y PREPARA PARA EL ENTRENAMIENTO O LA PREDICCION, DEVUELVE UN DATASET LIMPIO.'''
    # 1)Primero analizo los null
    # Total de null de todos los campos (1,23% de la base son null )
    # dataset_crudo.isnull().sum().sum()

    # Total de null por campo
    # dataset_crudo.isnull().sum()

    # dataset_crudo.isna().sum()

    # Resumen la tendencia central, la dispersión y la forma de la distribución de un conjunto de datos, excluyendo los valores NaN.

    # dataset_crudo.describe()

    #  Se elimina el id porque no es significativo (No es significativo a la hr de entrenar el modelo)
    dataset_crudo = dataset_crudo.drop(columns='id')

    # Reemplazamos los nulos en edad por la media
    media_edad = dataset_crudo.edad.mean()
    dataset_crudo["edad"] = dataset_crudo["edad"].fillna(media_edad)

    # Otra vez isnull para ver que efectivamente fueron reemplazados
    # dataset_crudo.isnull().sum()

    # Reemplazmos los anos_edc por su media
    anos_media = dataset_crudo.anos_edc.mean()
    dataset_crudo.anos_edc = dataset_crudo.anos_edc.fillna(anos_media)
    # vemos la info para ver si fue reemplazada y ya no es null
    # dataset_crudo.isnull().sum()

    # Hacemos lo mismo para etnia solo que lo reemplazamos por "sin_rec_etnico"
    sin_etnia = "sin_rec_etnico"
    dataset_crudo.etnia = dataset_crudo.etnia.fillna(sin_etnia)
    # verificamos
    # dataset_crudo.isnull().sum()

    # importante saber el Dtype de cada columna para normalizar
    # Los datos de tipo  Object (1 Sexo, 5 Estudiante act, 9 Etnia, 10 Padres_reside) los pasamos a Numericos...
    # dataset_crudo.info()

    # Devuelve la cantidad de valores unicos por campo de df
    # dataset_crudo.nunique(axis=0)

    # ETNIA
    # Devuelve los valores unico de un campo
    # print('Etnia = {}'.format(dataset_crudo.etnia.unique()))

    # type(dataset_crudo.etnia)
    # Devuelve cuales son los valores unico de un campo
    # dataset_crudo.etnia.unique()

    # SEXO
    # print(dataset_crudo.sexo.unique())

    # Contamos los valores unicos (Para ver cual es el que predomina)
    # print(dataset_crudo["sexo"].value_counts())

    # Normalizo string
    dataset_crudo.sexo = dataset_crudo.sexo.replace(['Mujer'], 'MUJER')
    dataset_crudo.sexo = dataset_crudo.sexo.replace(['Hombre'], 'HOMBRE')
    # Vuelvo a ver como quedo
    # dataset_crudo.sexo.unique()

    # Reemplazamos a Mujer=0 Hombre=1

    # PROBLEMA 1 QUE SE PRESENTA ---> Como definimos que 0=mujer y 1=hombre?
    dataset_crudo.sexo = dataset_crudo.sexo.replace(['MUJER'], 0)
    dataset_crudo.sexo = dataset_crudo.sexo.replace(['HOMBRE'], 1)
    dataset_crudo.sexo = dataset_crudo.sexo.replace(['0'], 0)
    dataset_crudo.sexo = dataset_crudo.sexo.replace(['1'], 0)
    # Vuelvo a ver como quedo
    # dataset_crudo.sexo.unique()

    # ESTUDIANTE
    # dataset_crudo.estudiante_act.unique()

    dataset_crudo.estudiante_act = dataset_crudo.estudiante_act.replace(['No', 'NO'], 0)
    dataset_crudo.estudiante_act = dataset_crudo.estudiante_act.replace(['Si', 'SI', 'SIPI'], 1)
    # dataset_crudo.estudiante_act.unique()

    # PADRE RESIDE
    # dataset_crudo.nunique(axis=0)
    # dataset_crudo.padres_reside.unique()

    # ESTRATO
    # dataset_crudo.estrato.unique()

    # dataset_crudo.nunique(axis=0)

    # dataset_crudo.info()

    dataset_curado = dataset_crudo

    # Guarda el DF CURADO en un archivo csv
    # ver_directorio_actual()
    # dataset_curado.to_csv('static/dataset_curado_1.csv', index=False)

    # get_dummies convierte la variable categórica en variables ficticias/indicadoras (por cada categoria agrega una columna).
    dataset_curado_2 = pd.get_dummies(dataset_curado, columns=['padres_reside'])
    # dataset_curado_2

    dataset_curado_2 = pd.get_dummies(dataset_curado_2, columns=['etnia'])
    # dataset_curado_2

    # dataset_curado_2.info()

    # Guarda el DF CURADO en un archivo csv
    # print('Estoy en el siguiente directorio: ', ver_directorio_actual())
    # dataset_curado_2.to_csv('static/dataset_curado_2.csv', index=False)
    print("FINALIZA EL PROCESO DE CLEANING")
    return dataset_curado_2

def test_tiempo_ejecucion_leer_csv_crudo():
    # ver_directorio_actual()
    inicio = time.time()
    path = "data/train.csv"
    dataset_crudo = leer_csv(path)
    fin = time.time()
    tiempo_ejecucion_ms = (fin - inicio) * 1000  # Convertir a milisegundos
    assert tiempo_ejecucion_ms <= 10, "LEER CSV A DF_CRUDO: El tiempo de ejecución supera los 10 ms"

def test_tiempo_ejecucion_cleaning_df_crudo():
    path = "data/train.csv"
    dataset_crudo = leer_csv(path)
    inicio = time.time()
    df_curado = data_cleaning(dataset_crudo)
    fin = time.time()
    tiempo_ejecucion_ms = (fin - inicio) * 1000  # Convertir a milisegundos
    assert tiempo_ejecucion_ms <= 10, "DATACLEANING: El tiempo de ejecución supera los 10 ms"



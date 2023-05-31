#  Importo librerias
import pandas as pd
# import numpy as np
from sklearn import preprocessing
from sklearn import tree
# from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from modelo_best_param import busqueda_best_parametros_grilla
from modelo_best_param import armar_parametros
# from sklearn.model_selection import GridSearchCV
import os


def ver_directorio_actual():
    directorio_actual = os.getcwd()
    print("Directorio actual:", directorio_actual)



"""# OBTENCIÓN DEL DATA SET"""


# Lee el csv y lo convierte a un df de pandas
# path = "/data/train.csv"
ver_directorio_actual()
path = "flaskapp/data/train.csv"
dataset_crudo = pd.read_csv(path)
dataset_crudo

"""# DATA CLEANING




"""

# 1)Primero analizo los null
# Total de null de todos los campos (1,23% de la base son null )
dataset_crudo.isnull().sum().sum()

# Total de null por campo
dataset_crudo.isnull().sum()

dataset_crudo.isna().sum()

# Resumen la tendencia central, la dispersión y la forma de la distribución de un conjunto de datos, excluyendo los valores NaN.

dataset_crudo.describe()

#  Se elimina el id porque no es significativo (No es significativo a la hr de entrenar el modelo)
dataset_crudo = dataset_crudo.drop(columns='id')

# Reemplazamos los nulos en edad por la media
media_edad = dataset_crudo.edad.mean()
dataset_crudo["edad"] = dataset_crudo["edad"].fillna(media_edad)

# Otra vez isnull para ver que efectivamente fueron reemplazados
dataset_crudo.isnull().sum()

# Reemplazmos los anos_edc por su media
anos_media = dataset_crudo.anos_edc.mean()
dataset_crudo.anos_edc = dataset_crudo.anos_edc.fillna(anos_media)
# vemos la info para ver si fue reemplazada y ya no es null
dataset_crudo.isnull().sum()

# Hacemos lo mismo para etnia solo que lo reemplazamos por "sin_rec_etnico"
sin_etnia = "sin_rec_etnico"
dataset_crudo.etnia = dataset_crudo.etnia.fillna(sin_etnia)
# verificamos
dataset_crudo.isnull().sum()

# importante saber el Dtype de cada columna para normalizar
# Los datos de tipo  Object (1 Sexo, 5 Estudiante act, 9 Etnia, 10 Padres_reside) los pasamos a Numericos...
dataset_crudo.info()

# Devuelve la cantidad de valores unicos por campo de df
dataset_crudo.nunique(axis=0)

# ETNIA
# Devuelve los valores unico de un campo
print('Etnia = {}'.format(dataset_crudo.etnia.unique()))

type(dataset_crudo.etnia)
# Devuelve cuales son los valores unico de un campo
dataset_crudo.etnia.unique()

# SEXO
print(dataset_crudo.sexo.unique())

# Contamos los valores unicos (Para ver cual es el que predomina)
print(dataset_crudo["sexo"].value_counts())

# Normalizo string
dataset_crudo.sexo = dataset_crudo.sexo.replace(['Mujer'], 'MUJER')
dataset_crudo.sexo = dataset_crudo.sexo.replace(['Hombre'], 'HOMBRE')
# Vuelvo a ver como quedo
dataset_crudo.sexo.unique()

# Reemplazamos a Mujer=0 Hombre=1

# PROBLEMA 1 QUE SE PRESENTA ---> Como definimos que 0=mujer y 1=hombre?
dataset_crudo.sexo = dataset_crudo.sexo.replace(['MUJER'], 0)
dataset_crudo.sexo = dataset_crudo.sexo.replace(['HOMBRE'], 1)
dataset_crudo.sexo = dataset_crudo.sexo.replace(['0'], 0)
dataset_crudo.sexo = dataset_crudo.sexo.replace(['1'], 0)
# Vuelvo a ver como quedo
dataset_crudo.sexo.unique()

# ESTUDIANTE
dataset_crudo.estudiante_act.unique()

dataset_crudo.estudiante_act = dataset_crudo.estudiante_act.replace(['No', 'NO'], 0)
dataset_crudo.estudiante_act = dataset_crudo.estudiante_act.replace(['Si', 'SI', 'SIPI'], 1)
dataset_crudo.estudiante_act.unique()

# PADRE RESIDE
dataset_crudo.nunique(axis=0)
dataset_crudo.padres_reside.unique()

# ESTRATO
dataset_crudo.estrato.unique()

dataset_crudo.nunique(axis=0)

dataset_crudo.info()

dataset_curado = dataset_crudo

# Guarda el DF CURADO en un archivo csv
# ver_directorio_actual()
dataset_curado.to_csv('flaskapp/static/dataset_curado_1.csv', index=False)

# get_dummies convierte la variable categórica en variables ficticias/indicadoras (por cada categoria agrega una columna).
dataset_curado_2 = pd.get_dummies(dataset_curado, columns=['padres_reside'])
# dataset_curado_2

dataset_curado_2 = pd.get_dummies(dataset_curado_2, columns=['etnia'])
# dataset_curado_2

dataset_curado_2.info()

# Guarda el DF CURADO en un archivo csv
# print('Estoy en el siguiente directorio: ', ver_directorio_actual())
dataset_curado_2.to_csv('flaskapp/static/dataset_curado_2.csv', index=False)

"""# **MODELO: ARBOL DE DESICIÓN (DT)**"""

dataset_curado_KDD = dataset_curado_2

# Dividimos los datos
input = dataset_curado_KDD.drop(columns='empleado')
target = dataset_curado_KDD['empleado']
datos_train, datos_test, target_train, target_test = train_test_split(input, target, test_size=0.2, random_state=42)

# Normalizamos el dataset
min_max_scaler = preprocessing.MinMaxScaler()
datos_train_normalizado = min_max_scaler.fit_transform(datos_train)
datos_test_normalizado = min_max_scaler.fit_transform(datos_test)

# print(datos_test)
datos_test.to_csv('flaskapp/data/datos_test_prediccion.csv', index=False)

# Crea CSV con parametros
# busqueda_best_parametros_grilla(datos_train_normalizado, target_train)

# leo csv con best parametros para  HACER TEST UNITARIO
best_param_load = pd.read_csv('flaskapp/data/df_param.csv')

# obtengo los parametros y los guardo en las variables
criterion, max_depth, min_samples_leaf, min_samples_split, n_estimators = armar_parametros(best_param_load['best_params'][0])

# entreno el modelo con los mejores parametros de Random Forest 
random_forest = RandomForestClassifier(criterion=criterion, max_depth=max_depth, min_samples_leaf=min_samples_leaf, min_samples_split=min_samples_split, n_estimators=n_estimators).fit(datos_train_normalizado, target_train)

# obtengo los parametros y los guardo en las variables pero con los parametros de DECISIONTREE
criterion, max_depth, min_samples_leaf, min_samples_split, n_estimators = armar_parametros(best_param_load['best_params'][1])
# ENTRENO EL MODELO
decision_tree = tree.DecisionTreeClassifier(criterion=criterion, max_depth=max_depth, min_samples_leaf=min_samples_leaf, min_samples_split=min_samples_split).fit(datos_train_normalizado, target_train)


# Entrena el modelo con los parametros definidos por el csv de best param

print("############### PROCESO DE ENTRENAMIENTO FINALIZADO #########################")

# Entrenamos (con los datos del TRAIN) los modelos con las metricas obtenidas de la grilla
# decision_tree = tree.DecisionTreeClassifier(criterion='gini', max_depth=150, min_samples_leaf=10, min_samples_split=10).fit(datos_train_normalizado, target_train)

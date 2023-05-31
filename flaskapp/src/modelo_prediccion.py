

"""#LIBRERIAS"""

# Importo librerias
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sn
# from sklearn import preprocessing
# from sklearn import tree
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import accuracy_score
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import GridSearchCV
from modelo_entrenamiento import random_forest
from modelo_entrenamiento import decision_tree

"""#OBTENCIÓN DEL DATA SET"""
print("#################################   COMIENZA LA PREDICCION ############################################")
# Lee el csv y lo convierte a un df de pandas
path = "flaskapp/data/datos_test_prediccion.csv"
dataset_crudo = pd.read_csv(path)
# dataset_crudo

datos_test_normalizado = dataset_crudo
# print(datos_test_normalizado.head)

"""#**MODELO: ARBOL DE DESICIÓN (DT)**"""
# import os
# ruta_archivo = os.path.abspath("modelo_entrenamiento.py")
# print(ruta_archivo)
# from "C:\\Users\\Vir\\Desktop\\SDIA\\2-CIENTIFICO DE DATOS\\PP2\\PP2_MODELO_DT\\PP2_MODELO" ; import random_forest
# Predecimos con los datos del TEST
random_forest_prediction = random_forest.predict(datos_test_normalizado)
decision_tree_prediction = decision_tree.predict(datos_test_normalizado)

print("\n","########### PREDICCION ###############")

print("print random_forest_prediction : ", random_forest_prediction)
print("print decision_tree_prediction : ", decision_tree_prediction)

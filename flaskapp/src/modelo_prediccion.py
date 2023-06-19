

"""#LIBRERIAS"""

# Importo librerias
import pandas as pd
from src.modelo_entrenamiento import data_cleaning
from sklearn import preprocessing
import pandas as pd
import numpy as np
import pickle
import os
from src.modelo_entrenamiento import split_scaler_fit_modelo
# from src.modelo_entrenamiento import decision_tree

# 1 - Levantar el modelo guardado en la carpeta data
# 2 - recibir y/o levantar archivo para realizar prediccion
# 3 - Realizar prediccion.
# 4 - Devolver df con prediccion. (GUARDAR)



def leer_csv_prediccion(url):
    ''' Esta funcion recibe como parametro una url de archivo .csv.
    1 - Va a buscar el archivo en la ruta.
    2 - Va aplicar un cleaning a la planilla
    3 - Escala los datos.
    Devuelve un df listo para predecir, y los headers'''
    path = str(url)
    print(path, os.getcwd())
    dataset_crudo = pd.read_csv(path)
    dataset_normalizado = data_cleaning(dataset_crudo)
    headres = dataset_normalizado.columns
    # Normalizamos el dataset
    min_max_scaler = preprocessing.MinMaxScaler()
    dataset_normalizado2 = min_max_scaler.fit_transform(dataset_normalizado)
     # Convertir el array en un DataFrame
    df = pd.DataFrame(dataset_normalizado)
    df.to_csv('data/datos_test_normalizado2.csv', index=False)
    return dataset_normalizado2, headres
 

def levantar_modelo_guardado(models,dataset_normalizado, headers):
    ''' Recibe como parametro MODEL que puede ser rf o dt
        y un DF normalizado para la prediccion
        1 - identifica que modelo se quiere usar.
        2 - Se levanta el modelo guardado en la carpeta modelo/rf/modelo_entrenado_x.sav.
        3 - Predice los datos pasados en dataset_normalizado.
        4 - Se crea una columna prediccion en dataset_normalizado con la prediccion.'''
    dataset_normalizado2 = dataset_normalizado
    headers = headers
    directorio_actual = os.getcwd()
    print( directorio_actual ,"rf - dt" ,models["dt"] )
    
    # DECLARO PREDS
    preds = np.array([0] * len(dataset_normalizado2))

    if models["rf"] > 0:
        print("#################### ENTRA EN IF RF #########################")
        rf = pickle.load(open(os.path.join("modelo/rf/modelo_entrenado_rf_.sav"), 'rb'))
        #rf.fit(X_train_scaled, y_train)
        # preds = np.add(preds, np.array(list(rf.predict(dataset_normalizado2) * models["rf"])))
        preds = np.add(preds, np.array(list(rf.predict(dataset_normalizado2))))
        print(type(preds))

    if models["dt"] > 0:
        dt = pickle.load(open(os.path.join("modelo/dt/modelo_entrenado_dt_.sav"), 'rb'))
        #rf.fit(X_train_scaled, y_train)
        # preds = np.add(preds, np.array(list(dt.predict(dataset_normalizado2) * models["dt"])))
        preds = np.add(preds, np.array(list(dt.predict(dataset_normalizado2))))
    
    # Convertir el array en un DataFrame
    df = pd.DataFrame(dataset_normalizado)
    df.columns = headers
    print(df.columns)


    # Crear una columna con los valores de preds
    # preds = np.array([0] * len(df))  # Ejemplo de valores de preds
    df['prediccion'] = preds
    # dataset_normalizado2.insert(-1, 'prediccion', preds)
    return df



# """#OBTENCIÓN DEL DATA SET"""
# print("#################################   COMIENZA LA PREDICCION ############################################")
# # Lee el csv y lo convierte a un df de pandas
# path = "data/datos_test_prediccion.csv"
# dataset_crudo = pd.read_csv(path)
# # dataset_crudo

# datos_test_normalizado = dataset_crudo
# # print(datos_test_normalizado.head)

# """#**MODELO: ARBOL DE DESICIÓN (DT)**"""
# # import os
# # ruta_archivo = os.path.abspath("modelo_entrenamiento.py")
# # print(ruta_archivo)
# # from "C:\\Users\\Vir\\Desktop\\SDIA\\2-CIENTIFICO DE DATOS\\PP2\\PP2_MODELO_DT\\PP2_MODELO" ; import random_forest
# # Predecimos con los datos del TEST
# random_forest_prediction = random_forest.predict(datos_test_normalizado)
# decision_tree_prediction = decision_tree.predict(datos_test_normalizado)

# print("\n","########### PREDICCION ###############")

# print("print random_forest_prediction : ", random_forest_prediction)
# print("print decision_tree_prediction : ", decision_tree_prediction)
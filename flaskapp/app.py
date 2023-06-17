from flask import Flask, request
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import os
import numpy as np
from flask_cors import CORS
from xgboost import XGBRegressor
# from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from src.modelo_entrenamiento import *
from src.modelo_prediccion import leer_csv_prediccion, levantar_modelo_guardado 
import datetime

# app = Flask(__name__, static_url_path='/modelo')
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://192.168.100.150:3000"}})
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

models = {
  "rf": 1,
  "dt": 0,
  "xgb": 0,
  "lgbm": 0,
  "blend": False
}
url_prediccion = 'datos_entrada/ds_para_predecir.csv' 

ds_normalizado = leer_csv_prediccion(url_prediccion)
resulado_prediccion = levantar_modelo_guardado(models, ds_normalizado)
fecha_actual = datetime.datetime.now()
fecha_str = fecha_actual.strftime("%Y-%m-%d_%H-%M")
resulado_prediccion.to_csv('datos_salida/prediccion_'+fecha_str+'.csv', sep=';' )

@app.route('/prediction', methods=['POST'])
def hello_world():
# def prediccion():
    print("Hola prediccion")
    out =''
    try:
        url_prediccion = 'datos_entrada/ds_para_predecir.csv' 
        ds_normalizado = leer_csv_prediccion(url_prediccion)
        models = request.json   
        
        if models["blend"]:
            print('Entra en el if blend')
            resulado_prediccion = levantar_modelo_guardado(models, ds_normalizado)
            fecha_actual = datetime.datetime.now()
            fecha_str = fecha_actual.strftime("%Y-%m-%d_%H-%M")
            resulado_prediccion.to_csv('datos_salida/prediccion_'+fecha_str+'.csv', sep=';' )
 
            # preds = np.array([0] * 291)

            # if models["rf"] > 0:
            #     out += 'Entra en rf \n'
            #     rf = pickle.load(open(os.path.join("modelo/rf/", "modelo_entrenado_rf.sav"), 'rb'))
            #     #rf.fit(X_train_scaled, y_train)
            #     preds = np.add(preds, np.array(list(rf.predict(ds_normalizado) * models["rf"])))

            # if models["dt"] > 0:
            #     out += 'Entra en dt \n'
            #     rf = pickle.load(open(os.path.join("modelo/dt/", "modelo_entrenado_dt.sav"), 'rb'))
            #     #rf.fit(X_train_scaled, y_train)
            #     preds = np.add(preds, np.array(list(rf.predict(ds_normalizado) * models["dt"])))


            # mse = mean_squared_error(y_val, preds) ** 0.5

            # print(" EL MODELO YA PREDIJO, Su resultado es: ", preds)
            # out = str(mse)
            # return str(mse)

        else:
            print("Entra en el else de blend")
            if models["rf"] == 1.0:
                resulado_prediccion = levantar_modelo_guardado(models, ds_normalizado)
                fecha_actual = datetime.datetime.now()
                fecha_str = fecha_actual.strftime("%Y-%m-%d_%H-%M")
                resulado_prediccion.to_csv('datos_salida/prediccion_'+fecha_str+'.csv', sep=';' )   
                # rf = pickle.load(open(os.path.join("modelo/rf/", "modelo_entrenado_rf.sav"), 'rb'))
                # #rf.fit(X_train_scaled, y_train)
                # preds = rf.predict(X_val_scaled)

            if models["dt"] == 1.0:
                resulado_prediccion = levantar_modelo_guardado(models, ds_normalizado)
                fecha_actual = datetime.datetime.now()
                fecha_str = fecha_actual.strftime("%Y-%m-%d_%H-%M")
                nombre_archivo = 'datos_salida/prediccion_'+fecha_str+'.csv'
                resulado_prediccion.to_csv(nombre_archivo, sep=';' )  
                # rf = pickle.load(open(os.path.join("modelo/dt/", "modelo_entrenado_dt.sav"), 'rb'))
                # #rf.fit(X_train_scaled, y_train)
                # preds = rf.predict(X_val_scaled)

            
            print(" EL MODELO YA PREDIJO, Su resultado lo encontrara en la carpeta datos_salida con el nombre :", nombre_archivo)
            
            return nombre_archivo
    except Exception as e:
        print("Error:", str(e))
        pass
        return str(out)



@app.route('/train', methods=['POST'])
def hello_world1():
# def entrenamiento():
    try:
        models = request.json
        data = pd.read_csv(os.path.join(app.static_folder, "dataset_curado_2.csv"))
        X = data.drop('empleado', axis=1)
        y = data['empleado']

        X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.8, random_state=13)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)

        # random_forest, decision_tree = split_scaler_fit_modelo(data)

        if models["model"] == "rf":
            rf = RandomForestClassifier(max_depth=models["maxDepth"], n_estimators=models["nEstimators"])
            rf.fit(X_train_scaled, y_train)
            preds = rf.predict(X_val_scaled)

        if models["model"] == "dt":
            dt = tree(max_depth=models["maxDepth"], n_estimators=models["nEstimators"])
            dt.fit(X_train_scaled, y_train)
            preds = dt.predict(X_val_scaled)

        if models["model"] == "xgb":
            xgb = XGBRegressor(booster='gbtree', objective='reg:squarederror', max_depth=models["maxDepth"], n_estimators=models["nEstimators"], learning_rate=models["learningRate"])
            xgb.fit(X_train_scaled, y_train)
            preds = xgb.predict(X_val_scaled)
            
        if models["model"] == "lgbm":
            lgbm = LGBMRegressor(boosting_type='gbdt',objective='regression', max_depth=models["maxDepth"], n_estimators=models["nEstimators"], learning_rate=models["learningRate"])
            lgbm.fit(X_train_scaled, y_train)
            preds = lgbm.predict(X_val_scaled)

        mse = mean_squared_error(y_val, preds) ** 0.5

        return str(mse)
    except:
        pass

    return str(mse)

        

        



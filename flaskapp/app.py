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
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from src.modelo_entrenamiento import random_forest
from src.modelo_entrenamiento import decision_tree

app = Flask(__name__, static_url_path='/modelo')
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/prediction', methods=['POST'])
# def hello_world():
def prediccion():
    try:
        models = request.json
        data = pd.read_csv(os.path.join("/static", "dataset_curado_2.csv"))
        X = data.drop('empleado', axis=1)
        y = data['empleado']

        X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.8, random_state=13)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        out =''
        
        if models["blend"]:
            preds = np.array([0] * 291)

            if models["rf"] > 0:
                rf = pickle.load(open(os.path.join("modelo/rf/", "modelo_entrenado_rf.sav"), 'rb'))
                #rf.fit(X_train_scaled, y_train)
                preds = np.add(preds, np.array(list(rf.predict(X_val_scaled) * models["rf"])))

            if models["dt"] > 0:
                rf = pickle.load(open(os.path.join("modelo/dt/", "modelo_entrenado_dt.sav"), 'rb'))
                #rf.fit(X_train_scaled, y_train)
                preds = np.add(preds, np.array(list(rf.predict(X_val_scaled) * models["rf"])))

            if models["xgb"] > 0:
                xgb = pickle.load(open(os.path.join(app.static_folder, "xgb.sav"), 'rb'))
                #xgb.fit(X_train_scaled, y_train)
                preds = np.add(preds, np.array(list(xgb.predict(X_val_scaled) * models["xgb"])))
                
            if models["lgbm"] > 0:
                lgbm = pickle.load(open(os.path.join(app.static_folder, "lgbm.sav"), 'rb'))
                #lgbm.fit(X_train_scaled, y_train)
                preds = np.add(preds, np.array(list(lgbm.predict(X_val_scaled) * models["lgbm"])))

            mse = mean_squared_error(y_val, preds) ** 0.5

            print(" EL MODELO YA PREDIJO, Su resultado es: ", preds)
            out = str(mse)
            return str(mse)

        else:
            if models["rf"] == 1.0:
                rf = pickle.load(open(os.path.join("modelo/rf/", "modelo_entrenado_rf.sav"), 'rb'))
                #rf.fit(X_train_scaled, y_train)
                preds = rf.predict(X_val_scaled)

            if models["dt"] == 1.0:
                rf = pickle.load(open(os.path.join("modelo/dt/", "modelo_entrenado_dt.sav"), 'rb'))
                #rf.fit(X_train_scaled, y_train)
                preds = rf.predict(X_val_scaled)

            if models["xgb"] == 1.0:
                xgb = pickle.load(open(os.path.join(app.static_folder, "xgb.sav"), 'rb'))
                #xgb.fit(X_train_scaled, y_train)
                preds = xgb.predict(X_val_scaled)
                
            if models["lgbm"] == 1.0:
                lgbm = pickle.load(open(os.path.join(app.static_folder, "lgbm.sav"), 'rb'))
                #lgbm.fit(X_train_scaled, y_train)
                preds = lgbm.predict(X_val_scaled)

            mse = mean_squared_error(y_val, preds) ** 0.5
            print(" EL MODELO YA PREDIJO, Su resultado es: ", preds)
            out = str(mse)
            return str(mse)
    except:
        pass

    return out


@app.route('/train', methods=['POST'])
# def hello_world1():
def entrenamiento():
    try:
        models = request.json
        data = pd.read_csv(os.path.join(app.static_folder, "dataset_curado_2.csv"))
        X = data.drop('empleado', axis=1)
        y = data['empleado']

        X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.8, random_state=13)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)

        if models["model"] == "rf":
            rf = random_forest(max_depth=models["maxDepth"], n_estimators=models["nEstimators"])
            rf.fit(X_train_scaled, y_train)
            preds = rf.predict(X_val_scaled)

        if models["model"] == "dt":
            dt = decision_tree(max_depth=models["maxDepth"], n_estimators=models["nEstimators"])
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

        

        



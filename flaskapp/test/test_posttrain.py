import unittest
import numpy as np
import os
import pickle
import pandas as pd

class TestInvarianza(unittest.TestCase):
    def setUp(self):
        # Declara los valores de prueba necesarios
        self.dataset_normalizado2 = pd.read_csv("flaskapp/data/datos_test_normalizado2.csv") # Dataset normalizado de prueba

        # Carga los modelos de RF y DT utilizando 'with open'
        with open(os.path.join("flaskapp/modelo/rf/modelo_entrenado_rf_.sav"), 'rb') as rf_file:
            self.rf_modelo = pickle.load(rf_file)
        with open(os.path.join("flaskapp/modelo/dt/modelo_entrenado_dt_.sav"), 'rb') as dt_file:
            self.dt_modelo = pickle.load(dt_file)

    

    def test_invarianza(self):
        # Ejecuta el código que quiero probar
        preds = np.array([0] * len(self.dataset_normalizado2))

        preds = np.add(preds, np.array(list(self.rf_modelo.predict(self.dataset_normalizado2))))
        print(type(preds))
        # Agrega las aserciones para verificar los resultados esperados
        self.assertIsInstance(preds, np.ndarray,"La prediccion no es un array numpy")
     
        preds = np.add(preds, np.array(list(self.dt_modelo.predict(self.dataset_normalizado2))))
        # Agrega las aserciones para verificar los resultados esperados
        self.assertIsInstance(preds, np.ndarray,"La prediccion no es un array numpy")
        self.assertIsNotNone(self.rf_modelo, "El modelo rf no fue cargado correctamente")
        self.assertIsNotNone(self.dt_modelo, "El modelo dt no fue cargado correctamente")     


if __name__ == '__main__':
    unittest.main()
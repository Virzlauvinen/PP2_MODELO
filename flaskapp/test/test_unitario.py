import unittest
import pandas as pd
#from src.modelo_entrenamiento import leer_csv



class TestLeerCSV(unittest.TestCase):

    def leer_csv(self,ruta_archivo_csv):
        url = str(ruta_archivo_csv)
        dataset_crudo = pd.read_csv(url)
        return dataset_crudo

    def test_leer_csv(self):
        ruta_archivo_csv = "flaskapp\datos_salida\prediccion_2023-06-26_13-38-06.csv"  # Coloca aquí la ruta de tu archivo CSV de prueba
        dataset = self.leer_csv(ruta_archivo_csv)
        # Verificar que el DataFrame tenga las columnas esperadas
        columnas_esperadas = ['id', 'sexo', 'edad', 'anos_edc', 'pareja', 'estudiante_act', 'estrato', 'pc', 'internet', 'etnia', 'padres_reside']
        self.assertListEqual(list(dataset.columns), columnas_esperadas)

if __name__ == '__main__':
    unittest.main()
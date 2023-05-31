#  Importo librerias
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import ast

# Generamos los parametros para hacer una busqueda en grilla del mejor modelo
def busqueda_best_parametros_grilla(datos_train_normalizado, target_train) :
    ''' La funcion busca los mejores parametros para modelo RandomForestClassifier() y tree.DecisionTreeClassifier
        Como parametros de entrada deben ingresar: 1 -> set de datos predictores train;  2 -> Set de datos target tain.
        Devuelve un archivo csv donde la los parametros se encontraran en ['best_params'][0] -> RandomForestClassifier y ['best_params'][1] -> DecisionTreeClassifier
    '''
    model_params = {
        'random_forest': {
            'model': RandomForestClassifier(),
            'params': {
                'n_estimators': [10, 25, 50],        # numero de arboles en el bosque
                'max_depth': [3, 5, 10, 50, 100, 150],             # profundidad maxima del arbol
                'min_samples_split': [10, 50],  # numero minimo de muestras requeridas para dividir un nodo interno
                'min_samples_leaf': [10, 50],   # numero minimo de muestras requeridas para estar en un nodo hoja
                'criterion': ['gini', 'entropy']
            }
        },
        'decision tree': {
            'model': tree.DecisionTreeClassifier(),
            'params': {
                'max_depth': [3, 5, 10, 50, 100, 150],
                'min_samples_split': [10, 50],
                'min_samples_leaf': [10, 50],
                'criterion': ['gini', 'entropy']
            }
        }
    }

    # Hacemos la busqueda en grilla
    score = []

    for model_name, mp in model_params.items():
        clf = GridSearchCV(mp['model'], mp['params'], cv=3, return_train_score=False)
        clf.fit(datos_train_normalizado, target_train)
        score.append({
            'model': model_name,
            'best_score': clf.best_score_,
            'best_params': clf.best_params_
        })

    # Vemos cuales fueron los mejores resultados de cada modelo y seleccionamos el mejor
    df_score = pd.DataFrame(score, columns=['model', 'best_score', 'best_params'])
    # df_score

    print(df_score['best_params'][0])
    print(df_score['best_params'][1])
    # Guardo df con besparametros en la carpeta data
    df_score.to_csv('flaskapp/data/df_param.csv', index=False)

def armar_parametros(cadena) :
    ''' Recibe una cadena de parametros de entrenamiento y format'''
    # Evaluar la cadena como una expresión de Python
    diccionario = ast.literal_eval(cadena)

    criterion = ''
    max_depth = 0
    min_samples_leaf = 0
    min_samples_split = 0
    n_estimators = 0

    # Recorrer el diccionario
    for key, value in diccionario.items():
        # Imprimir la clave y el valor
        print(key, ":", value)
        if key == 'criterion' :
            criterion = value
        elif key == 'max_depth' :
            max_depth = value
        elif key == 'min_samples_leaf' :
            min_samples_leaf = value
        elif key == 'min_samples_split' :
            min_samples_split = value
        elif key == 'n_estimators' :
            n_estimators = value

    # output = "criterion='"+criterion+"', max_depth="+str(max_depth)+", min_samples_leaf="+str(min_samples_leaf)+", min_samples_split="+str(min_samples_split)+", n_estimators="+str(n_estimators)
    return criterion, max_depth, min_samples_leaf, min_samples_split, n_estimators

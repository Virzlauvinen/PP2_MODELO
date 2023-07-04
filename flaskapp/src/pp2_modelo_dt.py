# -*- coding: utf-8 -*-
"""PP2_MODELO_DT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OhSsDg7YSEKCetuxY6xmemWHPUKdme7c
"""

#Vincula Colab con Drive (monta el Drive en la máquina virtual que nos provee Google)
# from google.colab import drive

# drive.mount('/content/DRIVE')

"""#REQUERIMIENTOS"""

#Importo librerias
import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn import tree
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

"""#OBTENCIÓN DEL DATA SET"""

#Lee el csv y lo convierte a un df de pandas
path = 'train.csv'
dataset_crudo = pd.read_csv(path)
dataset_crudo

"""#DATA CLEANING




"""

#1)Primero analizo los null
#Total de null de todos los campos (1,23% de la base son null )
dataset_crudo.isnull().sum().sum()

#Total de null por campo
dataset_crudo.isnull().sum()

dataset_crudo.isna().sum()

#Resumen la tendencia central, la dispersión y la forma de la distribución de un conjunto de datos, excluyendo los valores NaN.

dataset_crudo.describe()

# Se elimina el id porque no es significativo (No es significativo a la hr de entrenar el modelo)
dataset_crudo = dataset_crudo.drop(columns='id')

#Reemplazamos los nulos en edad por la media
media_edad=dataset_crudo.edad.mean()
dataset_crudo["edad"] = dataset_crudo["edad"].fillna(media_edad)

#Otra vez isnull para ver que efectivamente fueron reemplazados
dataset_crudo.isnull().sum()
print(dataset_crudo.head())
#Reemplazmos los anos_edc por su media
anos_media = dataset_crudo['anos_edc'].mean()
dataset_crudo.anos_edc = dataset_crudo.anos_edc.fillna(anos_media)
#vemos la info para ver si fue reemplazada y ya no es null
dataset_crudo.isnull().sum()

#Hacemos lo mismo para etnia solo que lo reemplazamos por "sin_rec_etnico"
sin_etnia = "sin_rec_etnico"
dataset_crudo.etnia = dataset_crudo.etnia.fillna(sin_etnia)
#verificamos
dataset_crudo.isnull().sum()

# importante saber el Dtype de cada columna para normalizar 
#Los datos de tipo  Object (1 Sexo, 5 Estudiante act, 9 Etnia, 10 Padres_reside) los pasamos a Numericos...
dataset_crudo.info()

#Devuelve la cantidad de valores unicos por campo de df
dataset_crudo.nunique(axis=0)

#ETNIA
#Devuelve los valores unico de un campo 
print('Etnia = {}'.format(dataset_crudo.etnia.unique()))

type(dataset_crudo.etnia)
#Devuelve cuales son los valores unico de un campo
dataset_crudo.etnia.unique()

#SEXO
print(dataset_crudo.sexo.unique())

#Contamos los valores unicos (Para ver cual es el que predomina)
print(dataset_crudo["sexo"].value_counts())

#Normalizo string
dataset_crudo.sexo = dataset_crudo.sexo.replace(['Mujer'], 'MUJER')
dataset_crudo.sexo =dataset_crudo.sexo.replace(['Hombre'], 'HOMBRE')
#Vuelvo a ver como quedo
dataset_crudo.sexo.unique()

#Reemplazamos a Mujer=0 Hombre=1

#PROBLEMA 1 QUE SE PRESENTA ---> Como definimos que 0=mujer y 1=hombre? 
dataset_crudo.sexo = dataset_crudo.sexo.replace(['MUJER'], 0)
dataset_crudo.sexo = dataset_crudo.sexo.replace(['HOMBRE'], 1)
dataset_crudo.sexo = dataset_crudo.sexo.replace(['0'], 0)
dataset_crudo.sexo = dataset_crudo.sexo.replace(['1'], 0)
#Vuelvo a ver como quedo
dataset_crudo.sexo.unique()

#ESTUDIANTE
dataset_crudo.estudiante_act.unique()

dataset_crudo.estudiante_act = dataset_crudo.estudiante_act.replace(['No', 'NO'], 0)
dataset_crudo.estudiante_act = dataset_crudo.estudiante_act.replace(['Si', 'SI', 'SIPI'], 1)
dataset_crudo.estudiante_act.unique()

#PADRE RESIDE
dataset_crudo.nunique(axis=0)
dataset_crudo.padres_reside.unique()

#ESTRATO
dataset_crudo.estrato.unique()

dataset_crudo.nunique(axis=0)

dataset_crudo.info()

dataset_curado = dataset_crudo

#Guarda el DF CURADO en un archivo csv
dataset_curado.to_csv('dataset_curado_1', index=False)

#get_dummies convierte la variable categórica en variables ficticias/indicadoras (por cada categoria agrega una columna).
dataset_curado_2 = pd.get_dummies(dataset_curado, columns=['padres_reside'])
dataset_curado_2

dataset_curado_2= pd.get_dummies(dataset_curado_2 , columns=['etnia'])
dataset_curado_2

dataset_curado_2.info()

#Guarda el DF CURADO en un archivo csv
dataset_curado_2.to_csv('dataset_curado_2', index=False)

"""#**MODELO: ARBOL DE DESICIÓN (DT)**"""

dataset_curado_KDD = dataset_curado_2

#Dividimos los datos
input = dataset_curado_KDD.drop(columns='empleado')
target = dataset_curado_KDD['empleado']
Datos_train, Datos_test, Target_train, Target_test = train_test_split (input, target, test_size= 0.2, random_state=42)

#Normalizamos el dataset 
min_max_scaler = preprocessing.MinMaxScaler()
Datos_train_normalizado = min_max_scaler.fit_transform(Datos_train)
Datos_test_normalizado = min_max_scaler.fit_transform(Datos_test)

"""##**Busqueda en Grilla de los mejores hiperparametros**

"""

#Generamos los parametros para hacer una busqueda en grilla del mejor modelo

model_params = {
    'random_forest':{
        'model':RandomForestClassifier(),
        'params':{
            'n_estimators':[10, 25, 50],        #numero de arboles en el bosque
            'max_depth':[3, 5,10,50,100,150],             #profundidad maxima del arbol
            'min_samples_split':[10, 50],  #numero minimo de muestras requeridas para dividir un nodo interno
            'min_samples_leaf':[10, 50],   #numero minimo de muestras requeridas para estar en un nodo hoja
            'criterion':['gini', 'entropy']
        }
    },
  'decision tree':{
      'model':tree.DecisionTreeClassifier(),
      'params':{
          'max_depth':[3, 5,10,50,100,150],
          'min_samples_split':[10, 50],
          'min_samples_leaf':[10, 50],
          'criterion':['gini','entropy']
      }
  }
}

#Hacemos la busqueda en grilla
score = []

for model_name, mp in model_params.items():

  clf=GridSearchCV(mp['model'],mp['params'], cv=3, return_train_score=False)
  clf.fit(Datos_train_normalizado, Target_train)
  
  score.append({
      'model':model_name,
      'best_score': clf.best_score_,
      'best_params': clf.best_params_
  })

#Vemos cuales fueron los mejores resultados de cada modelo y seleccionamos el mejor
df_score = pd.DataFrame(score, columns=['model', 'best_score', 'best_params'])
df_score

print(df_score['best_params'][0])
print(df_score['best_params'][1])

#Entrenamos (con los datos del TRAIN) los modelos con las metricas obtenidas de la grilla
random_forest = RandomForestClassifier(criterion= 'entropy', max_depth= 50, min_samples_leaf= 10, min_samples_split= 10, n_estimators= 50).fit(Datos_train_normalizado, Target_train)
decision_tree = tree.DecisionTreeClassifier(criterion= 'gini', max_depth= 150, min_samples_leaf= 10, min_samples_split= 10).fit(Datos_train_normalizado, Target_train)

#Predecimos con los datos del TEST
random_forest_prediction = random_forest.predict(Datos_test_normalizado)
decision_tree_prediction = decision_tree.predict(Datos_test_normalizado)

"""##**Metricas DT**"""

random_forest_accuracy = accuracy_score(Target_test, random_forest_prediction)
decision_tree_accuracy = accuracy_score(Target_test, decision_tree_prediction)

random_forest_accuracy

decision_tree_accuracy

plt.figure(figsize=(10,5))
ax = plt.subplot(1,2,1)
sns.heatmap(confusion_matrix(Target_test, random_forest_prediction), annot=True, fmt="g",  cmap="YlOrRd", cbar=False)
ax.set_xlabel('Prediction')
ax.set_ylabel('Target')
ax.set_title(f"Random Forest (Acc: {random_forest_accuracy:.4f})")
ax = plt.subplot(1,2,2)
sns.heatmap(confusion_matrix(Target_test, decision_tree_prediction), annot=True, fmt="g",  cmap="YlOrRd", cbar=False)
ax.set_xlabel('Prediction')
ax.set_ylabel('Target')
ax.set_title(f"Decision Tree (Acc: {decision_tree_accuracy:.4f})")

#Porque el random forest dio los mejores resultados vemos la importancia de los atributos para este modelo
importances = list(random_forest.feature_importances_)
input_list = list(input.columns)

feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(input_list,importances)]
feature_importances = sorted(feature_importances, key= lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances ];

plt.figure(figsize=(50,50))
_ = tree.plot_tree(random_forest.estimators_[0], feature_names=input.columns, filled=True, fontsize=18)

"""## **Conclusión DT**:
Al incrementar el parametro **max_depth** se obtiene mejores resultados en el entrenamiento y en la prediccion.
Sin embargo los modelos de desision_tree y random_forest no llegana  explicar mas del 70% de los casos.

Deberiamos trabajar en la poda del arbol para poder hacer mas legibles las regals con las que clasifica.
"""
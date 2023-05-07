## INSTALACION 
 [1] - Instalar Python 3.7 (la 10 y 11 andan mal) --> YO USE ANACONDA XQ SINO NO ANDABA
 [1B] -En requirements.txt borrar la version del pip
 [2] - Correr el requirements.txt
 pip install -r requirements.txt
 [3] - Agregar los CORS en el archivo app.py con el host de donde va a recibir la solicitud.
 esto se debe hacer para que el servidor de Flask acepte las peticiones del servidor de React.

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(_name_)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

[4] - Ejecutar el servidor flask con 
flask run 

[5] - Ejecutar el servidor de React (npm start).
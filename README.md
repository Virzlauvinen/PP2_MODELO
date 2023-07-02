# PRACTICA PROFESIONALIZANTE 2 (PP2) -  CLASIFICACIÓN DE LA ECONOMÍA LABORAL


**INTEGRANTE:** Virginia Zlauvinen


El objetivo del presente trabajo es hacer la puesta en producción y el posterior deployment del proyecto de practica profesionalizante 1 (PPT1_CLASIFICACIÓN DE LA ECONOMÍA LABORAL) en el cual se crearon diferentes algoritmos de clasificación que lograban categorizar a un grupo de individuos en empleado o desempleado. 

Para esto se seleccionaron los mejores modelos de la etapa anterior, Decision Tree y Random Forest y se utilizó un set de datos con 25424 observaciones y 12 variables con información relevante. La columna principal empleado toma el valor de 0 para individuos que no tienen empleo y 1 para los que si, el resto de columnas hace referencia a características propias de cada individuo.



# INSTALACION 

1 - Instalar Python 3.7 
 
EN UNA TERMINAL COMMAND PROMPT 

2 - Correr el requirements.txt ----> pip install -r requirements.txt
 

3 - Ejecutar Flaskapp 
- Abrí tu terminal o línea de comandos.
- Navega hasta el directorio raíz de tu proyecto de aplicación usando el comando cd flaskapp
- En el dirctorio flaskapp ejecutar el servidor flask con **flask run**
- (para apagar ctrl+c)


4 - Ejecutar Reactapp la aplicación en modo de desarrollo: Esto asume que tenes Node.js y npm (Node Package Manager) instalados en tu máquina. Si no los has instalado, debes hacerlo antes de realizar lo siguiente:

- Abre tu terminal o línea de comandos.
- Navega hasta el directorio raíz de tu proyecto de aplicación usando el comando cd reactapp
- Una vez dentro del directorio del proyecto, ejecuta el siguiente comando para iniciar el servidor de desarrollo React: **npm start**
- (para apagar ctrl+c)

Después de ejecutar npm start, el servidor de desarrollo compilará tu aplicación y la iniciará. También mostrará un mensaje indicando la URL donde puedes ver la aplicación en tu navegador, generalmente http://localhost:3000. Abre tu navegador  e ingresa la URL proporcionada.

La aplicación ahora se ejecutará en tu navegador. Cualquier cambio que realices en el código fuente provocará automáticamente una recarga de la página, lo que te permitirá ver la versión actualizada de tu aplicación.


**DIFICULTADES**

EN EL CASO DE PROLEMAS DE CONEXION

 Agregar los CORS en el archivo app.py con el host de donde va a recibir la solicitud.
 esto se debe hacer para que el servidor de Flask acepte las peticiones del servidor de React.

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(_name_)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

El botón de descarga no funciona todavia.
cuales son las unicas carpetas necesarias que tienen que ir al main para un posterior deployment





# PP2_MODELO
OBJETIVO: Hacer la puesta en produccion y el posterior deployment del proyecto PPT_CLASIFICACIÓN DE LA ECONOMÍA LABORAL
# CREAR REQUIEREMENT con pipreqs
El siguiente proceso muestra como crear un requierement de forma automatica con la libreria pipreqs.
Tener en cuenta que el requierement creado esta en la carpeta raiz del proyecto. Luego los archivos y el requierement deben ser ubicados en la carpeta raiz de python.
## PASOS
Si tiene un archivo .py que contiene el código de su proyecto junto con los import necesarios, puede utilizar una herramienta llamada "pipreqs" para generar un archivo requirements.txt basado en ese archivo .py. Siga los siguientes pasos para instalar y utilizar pipreqs:

1. Instale pipreqs: Abra una línea de comando y ejecute el siguiente comando:

```
pip install pipreqs

```
2. Genere el archivo requirements.txt: En la misma línea de comando, vaya al directorio que contiene su archivo .py y ejecute el siguiente comando:
Recuerde que debe ir  al directorio raiz

```
pipreqs .

```

Esto generará un archivo requirements.txt en el directorio actual, que contiene todas las dependencias que se encuentran en el archivo .py y sus versiones correspondientes.

Tenga en cuenta que pipreqs detectará automáticamente las dependencias requeridas por su proyecto y generará un archivo requirements.txt que las incluya. Sin embargo, puede haber algunas dependencias que pipreqs no detecte automáticamente y que deba agregar manualmente al archivo requirements.txt.

Es importante recordar que el archivo requirements.txt generado por pipreqs puede contener dependencias innecesarias o versiones obsoletas, por lo que siempre es recomendable revisar y editar el archivo manualmente para asegurarse de que solo contenga las dependencias necesarias y actualizadas para su proyecto.

## Detalles de la creacion.
Como nuestros archivos estan escritos en español el proceso de pipreqs no trabaja con utf8 es decir que no contempla caracteres del idioma español como la Ñ las tildas, etc. para ello si les sale un error similar a este:

```
ERROR: Failed on file: .\pp2_modelo_dt.py
Traceback (most recent call last):
...
  File "<unknown>", line 69
    aÃ±os_media = dataset_crudo.aÃ±os_edc.mean()

```
Se puede observar que se da el error que se da xq el proceso no identifica la ñ sino que lo lee como " Ã± ".
Para resolverlo remplazamos la " ñ " por " n " en todo el archivo.
Luego volvemos a correr el comando 
```
pipreqs . --force

```

para que vuelva a correr. 
Es importante revisar y validar que ese requirement se creo correctamente, xq puede que falte alguna dependencia. el log del proceso indica que se debe revisar la dependencia  con el siguiente mensaje 
```
WARNING: Import named "seaborn" not found locally. Trying to resolve it at the PyPI server.
WARNING: Import named "seaborn" was resolved to "seaborn:0.12.2" package (https://pypi.org/project/seaborn/).
Please, verify manually the final list of requirements.txt to avoid possible dependency confusions.
```

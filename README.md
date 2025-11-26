# Taller Spark MLlib – Computación de Alto Desempeño

Autor: Santiago Gil Gallego (Sgg)  
Fecha de entrega: 27 de noviembre de 2025  

Este repositorio contiene el desarrollo del Taller de Spark MLlib para la asignatura de Computación de Alto Desempeño. El objetivo es implementar un flujo completo de:

- Preprocesamiento de datos con Spark.
- Entrenamiento y evaluación de un modelo supervisado.
- Aplicación de técnicas no supervisadas (clustering).

Todo se ejecuta sobre un clúster de Apache Spark con almacenamiento HDFS, utilizando Jupyter Lab como entorno de trabajo.

---

## 1. Estructura del repositorio

La estructura propuesta del proyecto es la siguiente:

```text
taller-spark-mllib-sgg/
│
├── data/
│   ├── supervised/
│   │   ├── breast_cancer_sgg.csv
│   │   └── preprocessed_sgg/         (generado por Spark en formato Parquet)
│   │
│   └── unsupervised/
│       ├── iris_sgg.csv
│       └── preprocessed_sgg/         (generado por Spark en formato Parquet)
│
├── notebooks/
│   ├── 01_preprocesamiento_sgg.ipynb
│   ├── 02_supervisado_sgg.ipynb
│   └── 03_no_supervisado_sgg.ipynb
│
├── prepare_datasets_sgg.py
└── README.md

Notas:

La carpeta data/ contiene los datos de entrada (CSV) y los datos preprocesados (Parquet).

La carpeta notebooks/ contiene los cuadernos Jupyter exigidos en el taller.

El archivo prepare_datasets_sgg.py genera los CSV a partir de datasets clásicos de sklearn.

2. Requerimientos técnicos

Para ejecutar el taller en el entorno de HPC se requiere:

Sistema operativo Rocky Linux (o equivalente en el clúster).

Apache Spark instalado y configurado en modo clúster (Standalone).

HDFS activo y accesible desde los nodos del clúster.

Python 3.9 o superior.

PySpark instalado en el entorno de ejecución.

Jupyter Lab instalado y accesible desde el nodo master.

Acceso por SSH al cluster (para tunel SSH y acceso a Jupyter Lab).

3. Inicialización del clúster Spark

Desde el nodo master (por ejemplo, cad02-nfs002):

cd /nfs/condor/spark
./sbin/stop-all.sh
./sbin/start-all.sh
jps

El comando jps debería mostrar al menos un proceso Master.
En los nodos worker se debería ver un proceso Worker con jps.

Para verificar el estado del clúster, se puede consultar la interfaz web del master:

http://10.43.100.121:8080

La interfaz debería listar los workers activos, núcleos totales, memoria total y recursos utilizados.

4. Generación y carga de datasets
4.1. Generación de CSV en el sistema de archivos local

En el directorio raíz del repositorio:
cd ~/jupyter_notebooks_sgil/taller-spark-mllib-sgg
python prepare_datasets_sgg.py

Este script genera:

data/supervised/breast_cancer_sgg.csv

data/unsupervised/iris_sgg.csv

Estos archivos se almacenan en el sistema de archivos local del usuario.

4.2. Carga de CSV a HDFS

Para que Spark usando el clúster pueda leer los datos, es conveniente copiarlos a HDFS:
cd ~/jupyter_notebooks_sgil/taller-spark-mllib-sgg

hdfs dfs -mkdir -p data/supervised
hdfs dfs -mkdir -p data/unsupervised

hdfs dfs -put data/supervised/breast_cancer_sgg.csv data/supervised/
hdfs dfs -put data/unsupervised/iris_sgg.csv data/unsupervised/


Verificación:
hdfs dfs -ls data/supervised
hdfs dfs -ls data/unsupervised


5. Ejecución de Jupyter Lab en el nodo master

En el nodo master:
cd ~/jupyter_notebooks_sgil
jupyter lab --no-browser --ip=0.0.0.0 --port=8888

Desde la máquina local (por ejemplo, Windows en mi caso):
ssh -L 8888:localhost:8888 estudiante@10.43.100.121

y con ésto en el navegador se puede acceder:
http://localhost:8888

Desde ahí se puede acceder a la carpeta taller-spark-mllib-sgg/notebooks/ y abrir los cuadernos.

6. Descripción de los cuadernos
6.1. 01_preprocesamiento_sgg.ipynb

Objetivo: realizar el preprocesamiento de los datasets supervisado y no supervisado usando Spark MLlib.

Contenido principal:

Inicialización de una sesión Spark conectada al master (spark://10.43.100.121:7077) con configuración de recursos (cores, memoria).

Lectura de los archivos CSV desde HDFS:

data/supervised/breast_cancer_sgg.csv

data/unsupervised/iris_sgg.csv

Exploración básica de los datos:

Conteo de filas y columnas.

Descriptivos estadísticos.

Conteo de valores nulos por columna.

Limpieza de datos:

Eliminación de duplicados.

Relleno de valores nulos en columnas numéricas (si fuera necesario).

Construcción de características:

Uso de VectorAssembler para crear una columna de tipo vector (features_raw).

Uso de StandardScaler para normalizar las características (features).

Almacenamiento en formato Parquet en HDFS:

data/supervised/preprocessed_sgg

data/unsupervised/preprocessed_sgg

Este cuaderno produce las vistas minables que serán utilizadas por los otros cuadernos.

6.2. 02_supervisado_sgg.ipynb

Objetivo: entrenar y evaluar un modelo de clasificación supervisada usando Spark MLlib.

Contenido principal:

Inicialización de una sesión Spark conectada al clúster.

Lectura del dataset preprocesado supervisado desde HDFS:

data/supervised/preprocessed_sgg

División del dataset en entrenamiento y prueba usando randomSplit.

Entrenamiento de un modelo de regresión logística (LogisticRegression) sobre la columna features.

Cálculo de métricas de desempeño:

Accuracy mediante MulticlassClassificationEvaluator.

F1-score mediante MulticlassClassificationEvaluator.

AUC-ROC mediante BinaryClassificationEvaluator.

Construcción de una matriz de confusión simple usando groupBy(label, prediction).count().

El cuaderno cierra con un breve análisis de los resultados obtenidos y posibles mejoras (uso de otros modelos, ajuste de hiperparámetros, etc.).

6.3. 03_no_supervisado_sgg.ipynb

Objetivo: aplicar técnicas no supervisadas (clustering) sobre el dataset preprocesado para aprendizaje no supervisado.

Contenido principal:

Inicialización de una sesión Spark conectada al clúster.

Lectura del dataset preprocesado no supervisado desde HDFS:

data/unsupervised/preprocessed_sgg

Entrenamiento de modelos de clustering K-Means para múltiples valores de k (por ejemplo, 2, 3, 4, 5).

Evaluación de cada modelo usando la métrica de Silhouette (ClusteringEvaluator).

Selección del mejor valor de k según el valor de Silhouette.

Análisis de resultados:

Conteo de instancias por cluster (groupBy(prediction).count()).

Impresión de centroides de los clusters.

El cuaderno finaliza con una interpretación básica de los clusters obtenidos y propuestas de extensiones (otros algoritmos, reducción de dimensionalidad, etc.).


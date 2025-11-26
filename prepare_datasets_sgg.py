# prepare_datasets_sgg.py
# Genera los archivos CSV para usar con Spark MLlib

import os
import pandas as pd
from sklearn.datasets import load_breast_cancer, load_iris

# Asegurar carpetas
os.makedirs("data/supervised", exist_ok=True)
os.makedirs("data/unsupervised", exist_ok=True)

# ---------- Dataset supervisado: Breast Cancer ----------
bc = load_breast_cancer()
df_bc = pd.DataFrame(bc.data, columns=bc.feature_names)
df_bc["label"] = bc.target  # 0 = benign, 1 = malignant

supervised_path = "data/supervised/breast_cancer_sgg.csv"
df_bc.to_csv(supervised_path, index=False)
print(f"Dataset supervisado guardado en: {supervised_path}")

# ---------- Dataset no supervisado: Iris ----------
iris = load_iris()
df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
df_iris["target"] = iris.target
df_iris["species"] = [iris.target_names[i] for i in iris.target]

unsupervised_path = "data/unsupervised/iris_sgg.csv"
df_iris.to_csv(unsupervised_path, index=False)
print(f"Dataset no supervisado guardado en: {unsupervised_path}")

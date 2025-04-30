import pickle
import pandas as pd

# Cargamos el modelo y el codificador creado anteriormente 
with open("data/clf.zahoree", "rb") as f:
    model = pickle.load(f)

with open("data/encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# Creamos una función para predecir el turnover_score de acuerdo a nuestro modelo y codificador generado
def predict_scores(df: pd.DataFrame) -> pd.DataFrame:
    cat_cols = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'OverTime']

    # Debugs
    # print("Columnas antes de codificar:", df.columns.tolist())
    # print("Columnas categóricas detectadas:", cat_cols)

    # Creamos una copia solo para las variables usadas en el modelo
    X = df.copy()

    # Codificamos las categóricas en la copia
    X[cat_cols] = encoder.transform(X[cat_cols])

    # Hacemos predicción utilizando el modelo
    expected_cols = model.feature_names_in_
    X = X[expected_cols]  # Solo usamos estas para la predicción

    # Agregamos la predicción obtenida al DataFrame original
    df["turnover_score"] = model.predict_proba(X)[:, 1]

    return df
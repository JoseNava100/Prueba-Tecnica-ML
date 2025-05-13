import joblib
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from typing import List

def load_model_artifacts():
    try:
        model = joblib.load("data/best_model.zahoree")
        return model
    except FileNotFoundError as e:
        raise FileNotFoundError("No se encontraron los archivos del modelo. Asegúrate de haber entrenado el modelo primero.") from e

def predict_scores(df: pd.DataFrame) -> pd.DataFrame:

    # Cargar modelo
    model = load_model_artifacts()
    
    # Obtener las columnas esperadas por el modelo
    try:
        # Para sklearn >= 1.0
        expected_cols = model.feature_names_in_
    except AttributeError:
        # Para versiones anteriores
        expected_cols = model.named_steps['classifier'].feature_names_in_
    
    # Verificar que tenemos todas las columnas necesarias
    missing_cols = set(expected_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Faltan columnas requeridas: {missing_cols}")
    
    # Preprocesar y predecir
    try:
        # Obtener probabilidades de clase positiva (turnover)
        probas = model.predict_proba(df)[:, 1]
        df = df.copy()  # Evitar SettingWithCopyWarning
        df["turnover_score"] = probas
    except Exception as e:
        raise RuntimeError(f"Error al hacer predicciones: {str(e)}") from e
    
    return df
import joblib
import pandas as pd
import numpy as np

# Función para cargar el modelo entrenado
def load_model_artifacts():
    try:
        model = joblib.load("data/best_model.zahoree")
        return model
    except FileNotFoundError as e:
        raise FileNotFoundError("No se encontraron los archivos del modelo. Asegúrate de haber entrenado el modelo primero.") from e

# Función para predecir los scores de rotación
def predict_scores(df: pd.DataFrame) -> pd.DataFrame:

    # cargamos el modelo
    model = load_model_artifacts()
    
    # Indicamos que columnas se usaron durante el entrenamiento
    try:
        expected_cols = model.feature_names_in_
    except AttributeError:
        expected_cols = model.named_steps['classifier'].feature_names_in_
    
    # Verificamos que las colunas reuqeridas estén presentes en el DataFrame
    missing_cols = set(expected_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Faltan columnas requeridas: {missing_cols}")
    
    # Preprocesar y predecir
    try:
        probas = model.predict_proba(df)[:, 1]
        df = df.copy()  
        df["turnover_score"] = probas
    except Exception as e:
        raise RuntimeError(f"Error al hacer predicciones: {str(e)}") from e
    
    # Retornamos el DatFrame con la columna nueva "turnover_score"
    return df
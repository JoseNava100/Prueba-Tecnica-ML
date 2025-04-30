import pandas as pd
from app.model import predict_scores

# Funcion para cargar y procesar el CSV en la carpeta Data del archivo dado HR_Employee_Attrition.csv
def load_and_process_data(csv_path: str = "data/HR_Employee_Attrition.csv") -> pd.DataFrame:

    # Leemos el archivo que se define dentro de los atributos de la función 
    df = pd.read_csv(csv_path)

    # Realizamos una limpieza y codificación simple para las columnas categóricas
    for col in ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'OverTime']:
        df[col] = df[col].astype("object")

    # Calculamos el turnover_score de nuestro modelo realizado
    df = predict_scores(df)

    return df

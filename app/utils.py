import pandas as pd
from app.model import predict_scores
from typing import Optional

def load_and_process_data(csv_path: str = "data/HR_Employee_Attrition.csv", 
                         keep_employee_number: bool = True) -> pd.DataFrame:

    # Columnas a eliminar
    columns_to_drop = ["EmployeeCount", "Over18", "StandardHours"]
    
    try:
        # Leer datos
        df = pd.read_csv(csv_path)
        
        # Opcionalmente eliminar EmployeeNumber
        if not keep_employee_number:
            columns_to_drop.append("EmployeeNumber")
        
        # Eliminar columnas no necesarias
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
        
        # Asegurar tipos correctos para columnas categóricas
        categorical_cols = ['BusinessTravel', 'Department', 'EducationField',
                          'Gender', 'JobRole', 'MaritalStatus', 'OverTime']
        
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype("category")
            else:
                raise ValueError(f"Columna categórica requerida '{col}' no encontrada")
        
        # Generar predicciones
        df = predict_scores(df)
        
        return df
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")
    except Exception as e:
        raise RuntimeError(f"Error procesando datos: {str(e)}") from e
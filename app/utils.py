import pandas as pd
from app.model import predict_scores

# Función para cargar y procesar el DataFrame
def load_and_process_data(csv_path: str = "data/HR_Employee_Attrition.csv", 
                         keep_employee_number: bool = True) -> pd.DataFrame:

    # Eliminamos columnas innnecesarias para calcular el "turnover_score"
    columns_to_drop = ["EmployeeCount", "Over18", "StandardHours"]
    
    try:
        # Cargamos el DataFrame
        df = pd.read_csv(csv_path)
        
        # Si "keep_employee_number = False", se añade "EmployeeNumber" a las columnas que se eliminarán.
        if not keep_employee_number:
            columns_to_drop.append("EmployeeNumber")
        
        # Eliminamos solo aquellas columnas de "columns_to_drop" que realmente estén presentes en el archivo.
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
        
        # Aseguramos que las columnas categóricas estén en el formato correcto, si alguna columna falla o no esta presente, lanza un error
        categorical_cols = ['BusinessTravel', 'Department', 'EducationField',
                          'Gender', 'JobRole', 'MaritalStatus', 'OverTime']
        
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype("category")
            else:
                raise ValueError(f"Columna categórica requerida '{col}' no encontrada")
        
        # Llamomos la funcion de predicción para calcular el "turnover_score" de nuestro modelo
        df = predict_scores(df)
        
        # Retornamos el DataFrame con el nuevo "turnover_score"
        return df
    
    # Creamos excepciones para manejar errores comunes, como archivo no encontrado o errores de lectura
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")
    except Exception as e:
        raise RuntimeError(f"Error procesando datos: {str(e)}") from e
from app.database import get_connection
import pandas as pd

# Función para guardar el DataFrame en la base de datos
def save_dataframe_to_db(df: pd.DataFrame):
    
    # Abrimos la conexión a la base de datos y abrimos un cursor para ejecutar comandos
    conn = get_connection()
    cursor = conn.cursor()

    # Guardamos la lista de columnas disponibles en el DataFrame
    available_cols = df.columns.tolist()
    
    # Definimos las colunmas esperadas a recibir en la base de datos, tanto datos originales como el nuevo campo "turnover_score" 
    required_db_cols = [
        "Age", "Attrition", "BusinessTravel", "DailyRate", "Department",
        "DistanceFromHome", "Education", "EducationField", "EmployeeNumber",
        "EnvironmentSatisfaction", "Gender", "HourlyRate", "JobInvolvement",
        "JobLevel", "JobRole", "JobSatisfaction", "MaritalStatus",
        "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked", "OverTime",
        "PercentSalaryHike", "PerformanceRating", "RelationshipSatisfaction",
        "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear",
        "WorkLifeBalance", "YearsAtCompany", "YearsInCurrentRole",
        "YearsSinceLastPromotion", "YearsWithCurrManager", "turnover_score"
    ]

    # Filtramos las columnas disponibles y tomamos solo las que estan presentes en el DataFrame
    cols_to_use = [col for col in required_db_cols if col in available_cols]
    
    # Preparamos una consulta dinamicamente
    placeholders = ", ".join(["%s"] * len(cols_to_use))
    columns_str = ", ".join(cols_to_use)
    query = f"REPLACE INTO employees ({columns_str}) VALUES ({placeholders})"

    # Recorremos fila por fila el DataFrame y ejecutamos la consulta con los valores correspondientes, esto se convierte en una tupla para que coincida 
    # con los pleceholders de la consulta y guardamos en la base de datos
    try:
        for _, row in df[cols_to_use].iterrows():
            cursor.execute(query, tuple(row))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Error al guardar: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    
    print("\nDatos guardados exitosamente en la base de datos.")
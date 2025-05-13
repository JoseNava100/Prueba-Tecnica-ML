from app.database import get_connection
import pandas as pd
from typing import List

def save_dataframe_to_db(df: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()

    # Columnas que realmente tienes + turnover_score
    available_cols = df.columns.tolist()
    
    # Columnas requeridas en la BD (ajustadas a lo que realmente tienes)
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

    # Verificar y seleccionar solo las columnas disponibles
    cols_to_use = [col for col in required_db_cols if col in available_cols]
    
    # Preparar query dinámica
    placeholders = ", ".join(["%s"] * len(cols_to_use))
    columns_str = ", ".join(cols_to_use)
    query = f"REPLACE INTO employees ({columns_str}) VALUES ({placeholders})"

    try:
        # Insertar datos
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
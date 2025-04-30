from app.database import get_connection
import pandas as pd

# Función para guardar el dataset con el turnover_score a la base de datos 
def save_dataframe_to_db(df: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()

    # Debug para verificar las columnas del dataset antes y despues
    # print(f"Columnas del DataFrame: {df.columns.tolist()}")
    # print(f"Total de columnas ANTES de validar: {len(df.columns)}")

    # Arreglo de columnas esperadas por la tabla employees de la base de datos
    expected_cols = [
        "Age", "Attrition", "BusinessTravel", "DailyRate", "Department",
        "DistanceFromHome", "Education", "EducationField", "EmployeeCount",
        "EmployeeNumber", "EnvironmentSatisfaction", "Gender", "HourlyRate",
        "JobInvolvement", "JobLevel", "JobRole", "JobSatisfaction", "MaritalStatus",
        "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked", "Over18", "OverTime",
        "PercentSalaryHike", "PerformanceRating", "RelationshipSatisfaction",
        "StandardHours", "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear",
        "WorkLifeBalance", "YearsAtCompany", "YearsInCurrentRole", "YearsSinceLastPromotion",
        "YearsWithCurrManager", "turnover_score"
    ]

    # Validador para coincidir con las 36 columnas recibidas
    if len(df.columns) != 36:
        print("El número de columnas en el DataFrame no coincide con el número esperado (36 columnas).")
        return

    # Asegurar de que todas las columnas estén presentes y en el orden correcto
    df = df[expected_cols]

    print(f"Total de columnas después de reordenar: {len(df.columns)}")

    # Generador de marcadores %s dinámicamente según el número de columnas, esto para evitar poner de mas o poner menos
    placeholders = ", ".join(["%s"] * len(expected_cols))
    columns_str = ", ".join(expected_cols)

    # Query dinamicamente con los marcadores generados
    query = f"""
        REPLACE INTO employees ({columns_str})
        VALUES ({placeholders})
    """

    # Insertar cada fila
    for _, row in df.iterrows():
        values = tuple(row)
        print(f"Insertando fila con {len(values)} elementos.")
        cursor.execute(query, values)

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Cerrar la conexión y el cursor
    cursor.close()
    conn.close()
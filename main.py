from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import pandas as pd
from app.database import get_connection
from app.model import predict_scores

app = FastAPI()

class EmployeeCreate(BaseModel):
    EmployeeNumber: int
    Age: int
    Attrition: str
    BusinessTravel: str
    DailyRate: float
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: float
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: float
    MonthlyRate: float
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: float
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int

# Petición GET entrada
@app.get("/")
def root():
    return {"message": "API para empleados"}

# Petición Get Empleados
@app.get("/employees")
def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Petición GET Empleado por ID
@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees WHERE EmployeeNumber = %s", (employee_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return result

from fastapi import HTTPException
import pandas as pd
from typing import Dict, List

# Petición POST agregar Empleado
@app.post("/employee")
async def create_employee(employee: EmployeeCreate):
    conn = None
    try:
        # Convertimos los datos del empleado a DataFrame
        employee_dict = employee.dict()
        
        # Creamos el DataFrame en un solo registro
        df = pd.DataFrame([employee_dict])
        
        # Calculamos el "turnover_score" en base al modelo
        df_with_score = predict_scores(df)
        
        # Obtenemos el "turnover_score" calculado
        turnover_score = df_with_score["turnover_score"].iloc[0]
        employee_dict["turnover_score"] = turnover_score
        
        # Preparamos las columnas y placeholders para la consulta SQL dinamicamente
        columns = list(employee_dict.keys())
        placeholders = ["%s"] * len(columns)
        
        # Query dinamico para insertar el nuevo empleado
        query = f"""
            INSERT INTO employees ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
        """
        
        # Ejecutamos la inserción
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, list(employee_dict.values()))
        conn.commit()
        
        # Obtenemos el ID del nuevo empleado
        employee_id = cursor.lastrowid
        cursor.close()

        # Función para generar la visualización del score
        def generate_risk_analysis(score: float) -> Dict:

            # Determinamos el nivel de riesgo
            if score >= 0.7:
                risk_level = "Alto Riesgo"
                recommendation = "Acción prioritaria requerida"
            elif score >= 0.4:
                risk_level = "Riesgo Moderado"
                recommendation = "Monitoreo cercano recomendado"
            else:
                risk_level = "Bajo Riesgo"
                recommendation = "Situación estable"
            
            # Porcentaje formateado
            percentage = score * 100
            
            return {
                "risk_level": risk_level,
                "interpretation": f"Probabilidad de rotación: {percentage:.1f}%",
                "recommendation": recommendation,
                "percentage": round(percentage, 1)
            }

        # Generar el análisis de riesgo
        risk_analysis = generate_risk_analysis(turnover_score)
        
        # Retornamos una respuesta enriquecida
        return {
            "message": "Empleado creado exitosamente",
            "employee_id": employee_id,
            "turnover_score": round(turnover_score, 4),
            "risk_analysis": risk_analysis,
            "details": {
                "score_scale": "0-1 (Donde 1 es mayor riesgo)",
                "model_version": "1.0",
                "timestamp": pd.Timestamp.now().isoformat()
            }
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear empleado: {str(e)}"
        )
    finally:
        if conn and conn.is_connected():
            conn.close()
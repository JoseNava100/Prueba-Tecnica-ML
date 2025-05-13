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

# Petición test
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

# Petición POST agregar Empleado
@app.post("/employee")
async def create_employee(employee: EmployeeCreate):
    conn = None
    try:
        # Convertir los datos del empleado a DataFrame
        employee_dict = employee.dict()
        
        # Crear DataFrame de un solo registro
        df = pd.DataFrame([employee_dict])
        
        # Calcular el turnover_score
        df_with_score = predict_scores(df)
        
        # Obtener el score calculado
        turnover_score = df_with_score["turnover_score"].iloc[0]
        employee_dict["turnover_score"] = turnover_score
        
        # Columnas y placeholders para la consulta SQL
        columns = list(employee_dict.keys())
        placeholders = ["%s"] * len(columns)
        
        # Consulta SQL para insertar
        query = f"""
            INSERT INTO employees ({', '.join(columns)})
            VALUES ({', '.join(placeholders)})
        """
        
        # Ejecutar la inserción
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, list(employee_dict.values()))
        conn.commit()
        
        # Obtener el ID del nuevo empleado
        employee_id = cursor.lastrowid
        cursor.close()
        
        return {
            "message": "Empleado creado exitosamente",
            "employee_id": employee_id,
            "turnover_score": turnover_score
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
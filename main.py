from fastapi import FastAPI, HTTPException
from app.database import get_connection

app = FastAPI()

# Petición test
@app.get("/")
def root():
    return {"message": "API para empleados y turnover_score"}

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
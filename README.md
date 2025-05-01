# 💼 HR Employee Turnover Predictor - Machine Learning REST API

## 🧠 Descripción del Proyecto

Este proyecto es una solución al reto propuesto para un puesto de Backend/Support Engineer. El objetivo es crear un servicio de Machine Learning utilizando Python y Docker, empleando el dataset `HR_Employee_Attrition` para predecir la probabilidad de que un colaborador renuncie a la empresa (turnover).

La solución incluye:
- Un nuevo modelo ML (`clf.zahoree`) previamente entrenado ya que el dado tenia una versión anterior.
- Un servicio REST API con dos endpoints: `GET` y `POST` el endpoint POST aun en desarrollo.
- Almacenamiento persistente de datos en una base de datos MySQL.
- Contenedor Docker con todas las dependencias para facilitar su ejecución y despliegue.

---

## ⚙️ Funcionalidades de la API

### 📍 1. `GET /employees`
- **Descripción**: Devuelve el dato completo de un colaborador existente en la base de datos con el `turnover_score`.
- **Parámetro requerido**: N/A.
- **Respuesta**:
```json
{
  "employee_id": 1001,
  "turnover_score": 0.723,
  "recommendation": "Alto riesgo de rotación",
  ...
}
```

### 📍 2. `GET /employee/{employee_id}`
- **Descripción**: Devuelve el dato completo y el `turnover_score` de un colaborador existente en la base de datos.
- **Parámetro requerido**: `employee_id` (por query string).
- **Respuesta**:
```json
{
  "employee_id": 1001,
  "turnover_score": 0.723,
  "recommendation": "Alto riesgo de rotación"
}
```

## Instalación

1. Clona el proyecto:
   ```bash
   git clone https://github.com/JoseNava100/Prueba-Tecnica-ML.git
   cd Prueba-Tecnica-ML
   ```

2. Crea el entorno virtua en windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   ```bash
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=employee_db
   DB_USER=root
   DB_PASSWORD=password
   ```

5. Correr los archivos main_test.py y train_model para su uso:
   ```bash
   python main_test.py
   python train_model.py
   ```

6. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

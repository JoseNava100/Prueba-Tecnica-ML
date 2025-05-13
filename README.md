<p align="center">
  <a href="https://www.python.org/" target="_blank">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="120" alt="Python Logo">
  </a>
</p>

# Machine Learning Service

---

### Descripción del Proyecto

Este proyecto es una solución al reto propuesto para un puesto de Backend/Support Engineer. El objetivo es crear un servicio de Machine Learning utilizando Python y Docker, empleando el dataset `HR_Employee_Attrition` para predecir la probabilidad de que un colaborador renuncie a la empresa (turnover_score).

La solución incluye:
- Un nuevo modelo ML (`best_model.zahoree`) previamente entrenado ya que el dado tenia una versión anterior y no era compatible.
- Un servicio REST API con dos endpoints: `GET` y `POST`.
- MIgración persistente de datos en una base de datos MySQL.
- Contenedor Docker con todas las dependencias para facilitar su ejecución y despliegue.

---

### ⚙️ Peticiónes de la API REST

#### 1. `GET /employees`
- **Descripción**: Devuelve el dato completo de un colaborador existente en la base de datos con el `turnover_score`.
```json
{
  "employee_id": 1001,
  ...
  "turnover_score": 0.723
},
  ...
{
  "employee_id": 2000,
  ...
  "turnover_score": 0.423
}
```

#### 2. `GET /employee/{employee_id}`
- **Descripción**: Devuelve el dato completo y el `turnover_score` de un colaborador especifico existente en la base de datos.
- **Parámetro requerido**: `employee_id`.
```json
{
  "employee_id": 1001,
  ...
  "turnover_score": 0.723
}
```

#### 3. `POST /employee`
- **Descripción**: Devuelve el dato con el `EmployeeNumber` y el `turnover_score` del colaborador registrado exitosamente en la base de datos.
```json
{
    "message": "Empleado creado exitosamente",
    "employee_id": 3000,
    "turnover_score": 0.18734125685120243
}
```
---

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

5. Ejecutar los archivos siguientes para su uso:
   ```bash
   python main_model_random_forest.py
   python main_turnover_score.py
   python main_migration.py
   python main_save_data.py
   ```

6. Ejecuta el servidor y realiza las peticiones GET y POST:
   ```bash
   uvicorn main:app --reload
   ```

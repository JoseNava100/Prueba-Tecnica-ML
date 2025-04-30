from app.utils import load_and_process_data
from app.crud import save_dataframe_to_db

# Test para revisar que se cree el turnover_score para guardarlo en la base de datos de cada empleado
df = load_and_process_data()

# Test para guardar los empleados en la base de datos con el turnover_score
save_dataframe_to_db(df)

# Muestra de datos de EmployeeNumber y turnover_score, como la confirmacion de los datos guardados a la base de datos con el turnover_score del empledo
print(df[["EmployeeNumber", "turnover_score"]].head())
print("Datos guardados en la base de datos.")

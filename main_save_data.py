from app.utils import load_and_process_data
from app.crud import save_dataframe_to_db

df = load_and_process_data()

try:
    save_dataframe_to_db(df)
except Exception as e:
    print(f"Error al guardar en BD: {e}")
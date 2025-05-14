import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
import joblib

# Cargamos el DataFrame con los datos de los empleados, con manejo de excepciones en caso de errores comunes
try:
    df = pd.read_csv("data/HR_Employee_Attrition.csv")
except FileNotFoundError:
    raise FileNotFoundError("El archivo CSV no se encontró en la ruta especificada")

# Eliminamos columnas irrelevantes que no aportan al modelo 
columns_to_drop = ["EmployeeCount", "Over18", "StandardHours", "EmployeeNumber"]
df_clean = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

X = df_clean.drop(columns=["Attrition"]) # X: Todas las características excepto "Attrition".
y = df_clean["Attrition"].map({"Yes": 1, "No": 0}) # y: La variable objetivo ("Attrition") convertida a binario (1=Sí abandona, 0=No)

# Calculamos pesos automáticos para equilibrar las clases, útiles si hay muchos más "No" que "Yes"
classes = np.unique(y)
class_weights = compute_class_weight('balanced', classes=classes, y=y)
class_weight_dict = dict(zip(classes, class_weights))

# Dividimos los datos en 80% entrenamiento y 20% prueba.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y) # Aseguramos que la proporción de clases se mantenga en ambos subconjuntos

# Identificamos las columnas numéricas y categóricas por tipo de dato
numeric_cols = X_train.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X_train.select_dtypes(include=['object']).columns

# Las columnas numericas se dejan igual y las categoricas se convierten en variables "dummy" usando "OneHotEncoder", ignorando categorias desconocidas
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numeric_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# CReamos un pipeline procesando los datos y aplicando el clasificador RandomForest
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        class_weight=class_weight_dict,
        random_state=42,
        n_jobs=-1))
])

# Buscamos hiperparámetros con GridSearchCV para optimizar el modelo
param_grid = {
    'classifier__n_estimators': [100, 200], # Número de árboles en el bosque
    'classifier__max_depth': [None, 10], # Profundidad máxima de los árboles
    'classifier__min_samples_split': [2, 5] # Número mínimo de muestras requeridas para dividir un nodo
}

# Usamos GridSearchCV para encontrar la mejor combinación de hiperparámetros 
# Usa validación cruzada "cv=3" para probar distintas combinaciones de parámetros y encontrar la mejor
# "scoring=f1" se optimiza el F1 Score, que equilibra precisión esto ideal en casos desbalanceados
# "n_jobs=-1" usa todos los núcleos del procesador.
grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='f1', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Se obtiene el mejor modelo entrenado y se hace la predicción sobre los datos de prueba
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Mostramos metricas de evalución "precision", "recall", "f1-score", y "support" e imprime la matriz de confusión, 
# para saber cuántos se predijeron correctamente y cuántos se confundieron
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred))
print("\nMatriz de Confusión:")
print(confusion_matrix(y_test, y_pred))

# Guardamos el modelo entrenado en un archivo usando "joblib" para su uso posterior y confirmamos que se guardó correctamente
joblib.dump(best_model, "data/best_model.zahoree", compress=3)
print("\nModelo guardado con éxito.")

print(f"\nMejores parámetros: {grid_search.best_params_}") # Imprime los mejores hiperparámetros encontrados
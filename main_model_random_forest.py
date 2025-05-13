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

# 1. Carga el dataset desde un CSV, con manejo de errores si el archivo no existe o hay algun error.
try:
    df = pd.read_csv("data/HR_Employee_Attrition.csv")
except FileNotFoundError:
    raise FileNotFoundError("El archivo CSV no se encontró en la ruta especificada")

# 2. Elimina columnas irrelevantes que no aportan al modelo y se define X, y
columns_to_drop = ["EmployeeCount", "Over18", "StandardHours", "EmployeeNumber"]
df_clean = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

X = df_clean.drop(columns=["Attrition"]) # X: Todas las características excepto "Attrition".
y = df_clean["Attrition"].map({"Yes": 1, "No": 0}) # y: La variable objetivo ("Attrition") convertida a binario (1=Sí abandona, 0=No).

# 3. Calcula pesos automáticos para equilibrar las clases útil si hay muchos más "No" que "Yes".
classes = np.unique(y)
class_weights = compute_class_weight('balanced', classes=classes, y=y)
class_weight_dict = dict(zip(classes, class_weights))

# 4. Divide los datos en 80% entrenamiento y 20% prueba.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# 5. Preprocesamiento robusto
numeric_cols = X_train.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X_train.select_dtypes(include=['object']).columns

preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numeric_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# 6. Pipeline completo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        class_weight=class_weight_dict,
        random_state=42,
        n_jobs=-1))
])

# 7. Búsqueda de hiperparámetros (simplificada para ejemplo)
param_grid = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [None, 10],
    'classifier__min_samples_split': [2, 5]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='f1', n_jobs=-1)
grid_search.fit(X_train, y_train)

# 8. Evaluación
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred))
print("\nMatriz de Confusión:")
print(confusion_matrix(y_test, y_pred))

# 9. Guardado
joblib.dump(best_model, "data/best_model.zahoree", compress=3)
print(f"\nMejores parámetros: {grid_search.best_params_}")
print("Modelo guardado con éxito.")
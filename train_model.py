import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

# Leemos el DataSet
df = pd.read_csv("data/HR_Employee_Attrition.csv")

# Tratamos columnas que no utilizaremos
df = df.drop(columns=["EmployeeCount", "Over18", "StandardHours", "EmployeeNumber"])

# Separamos las variables X y Y y definimos 1 como Trabajando y 0 Despedido
X = df.drop(columns=["Attrition"])
y = df["Attrition"].map({"Yes": 1, "No": 0})

# Codificamos las variables categóricas
cat_cols = X.select_dtypes(include=["object"]).columns

# Utilizamos el OrdinalEncoder para el entramiento y transformamos 
encoder = OrdinalEncoder()
X[cat_cols] = encoder.fit_transform(X[cat_cols])

# Dividimos el dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamos el Modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Guardamos el modelo y el archivo encoder
with open("data/clf.zahoree", "wb") as f:
    pickle.dump(model, f)

with open("data/encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Modelo y encoder guardados con éxito.")

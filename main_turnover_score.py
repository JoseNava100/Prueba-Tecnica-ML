from app.utils import load_and_process_data

# Verificamos los "turnover_score"
df = load_and_process_data()

print(df[["EmployeeNumber", "turnover_score"]].head(5))

print("\nTop 10 empleados con mayor riesgo de rotación:")
high_risk = df[df["turnover_score"] > 0.7][["EmployeeNumber", "turnover_score", "Department", "JobRole", "YearsAtCompany", "JobSatisfaction"]]
print(high_risk.sort_values("turnover_score", ascending=False).head(10))


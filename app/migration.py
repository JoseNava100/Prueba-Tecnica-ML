from app.database import get_connection

def create_database_and_table():
    try:
        # Conexión sin especificar base de datos
        connection = get_connection(with_db=False)
        cursor = connection.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS hr_service")

        # Conectarse a la nueva base de datos
        connection.database = "hr_service"

        # Crear la tabla employees
        create_table_query = """ 
        CREATE TABLE IF NOT EXISTS employees (
            EmployeeNumber INT PRIMARY KEY AUTO_INCREMENT,
            Age INT,
            Attrition ENUM('Yes', 'No'),
            BusinessTravel VARCHAR(50),
            DailyRate DECIMAL(10, 2),
            Department VARCHAR(50),
            DistanceFromHome INT,
            Education INT,
            EducationField VARCHAR(50),
            EmployeeCount INT DEFAULT 1,
            EnvironmentSatisfaction INT,
            Gender ENUM('Male', 'Female'),
            HourlyRate DECIMAL(10, 2),
            JobInvolvement INT,
            JobLevel INT,
            JobRole VARCHAR(50),
            JobSatisfaction INT,
            MaritalStatus VARCHAR(20),
            MonthlyIncome DECIMAL(12, 2),
            MonthlyRate DECIMAL(10, 2),
            NumCompaniesWorked INT,
            Over18 ENUM('Y', 'N') DEFAULT 'Y',
            OverTime ENUM('Yes', 'No'),
            PercentSalaryHike DECIMAL(5, 2),
            PerformanceRating INT,
            RelationshipSatisfaction INT,
            StandardHours INT DEFAULT 80,
            StockOptionLevel INT,
            TotalWorkingYears INT,
            TrainingTimesLastYear INT,
            WorkLifeBalance INT,
            YearsAtCompany INT,
            YearsInCurrentRole INT,
            YearsSinceLastPromotion INT,
            YearsWithCurrManager INT,
            turnover_score FLOAT
        )
        """
        cursor.execute(create_table_query)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database_and_table()
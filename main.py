import sys
import MySQLdb
from faker import Faker
import pandas as pd
import matplotlib.pyplot as plt
# Datos de conexión
host = "localhost"
user = "root"
password = ""
database = "CompanyData"

# Conectar al servidor MySQL y a la base de datos CompanyData
try:
    db = MySQLdb.connect(host, user, password, database)
    cursor = db.cursor()
    print("Conexión correcta a la base de datos 'CompanyData'.")
except MySQLdb.Error as e:
    print("No se pudo conectar a la base de datos:", e)
    sys.exit(1)


# Crear la tabla EmployeePerformance
create_table_query = """
CREATE TABLE IF NOT EXISTS EmployeePerformance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    department VARCHAR(255),
    performance_score DECIMAL(5,2),
    years_with_company INT,
    salary DECIMAL(10,2)
)
"""
try:
    cursor.execute(create_table_query)
    print("Tabla 'EmployeePerformance' creada o ya existente.")
except MySQLdb.Error as e:
    print("No se pudo crear la tabla 'EmployeePerformance':", e)
    sys.exit(1)
# Crear instancia de Faker
fake = Faker()

# Insertar 1000 registros ficticios en la tabla EmployeePerformance
insert_query = """
INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
VALUES (%s, %s, %s, %s, %s)
"""

data = []
for _ in range(1000):
    employee_id = fake.random_int(min=1, max=10000)
    department = fake.random_element(elements=('HR', 'Engineering', 'Sales', 'Marketing', 'Finance'))
    performance_score = round(fake.random.uniform(0, 10), 2)
    years_with_company = fake.random_int(min=0, max=40)
    salary = round(fake.random.uniform(30000, 120000), 2)
    data.append((employee_id, department, performance_score, years_with_company, salary))

try:
    cursor.executemany(insert_query, data)
    db.commit()
    print("1000 registros insertados en la tabla 'EmployeePerformance'.")
except MySQLdb.Error as e:
    print(f"Error al insertar los registros: {e}")
    db.rollback()

# Consulta para extraer los datos de la tabla EmployeePerformance
query = "SELECT * FROM EmployeePerformance"

# Extraer los datos utilizando pandas
try:
    df = pd.read_sql(query, db)
    print("Datos extraídos correctamente.")
except Exception as e:
    print("Error al extraer los datos:", e)
    sys.exit(1)

# Mostrar los primeros 5 registros
print(df.head())
# Cerrar la conexión
cursor.close()
db.close()
print("Conexión cerrada.")

# Calcular estadísticas para cada departamento
stats = df.groupby('department')['performance_score'].agg(['mean', 'median', 'std']).reset_index()

# Calcular estadísticas para cada departamento
stats2 = df.groupby('department')['salary'].agg(['mean', 'median', 'std']).reset_index()

# Calcular el número total de empleados por departamento
employee_count = df.groupby('department').size().reset_index(name='total_employees')

# Limpiar datos eliminando filas con valores nulos
df.dropna(subset=['years_with_company', 'performance_score'], inplace=True)

# Calcular la correlación entre years_with_company y performance_score
correlation = df['years_with_company'].corr(df['performance_score'])

# Limpiar datos eliminando filas con valores nulos
df.dropna(subset=['salary', 'performance_score'], inplace=True)

# Calcular la correlación entre salary y performance_score
correlation2 = df['salary'].corr(df['performance_score'])


# Mostrar estadísticas
print("")
print("Estadisticaas por departamento:")
print(stats)

print("")
print("Estadisticas de salarios por departamentos:")
print(stats2)

# Mostrar el número total de empleados por departamento
print(" ")
print("numero total de empleados:")
print(employee_count)


# Mostrar la correlación
print("")
print(f"Correlación entre years_with_company y performance_score: {correlation:.2f}")



print("")
# Mostrar la correlación
print(f"Correlación entre salary y performance_score: {correlation2:.2f}")



# Visualización 1: Histograma del performance_score para cada departamento
plt.figure(figsize=(12, 6))
for department in df['department'].unique():
    subset = df[df['department'] == department]
    plt.hist(subset['performance_score'], bins=20, alpha=0.5, label=department)
plt.xlabel('Performance Score')
plt.ylabel('Frequency')
plt.title('Histograma del Performance Score por Departamento')
plt.legend(title='Departamento')
plt.grid(True)
plt.show()

# Visualización 2: Gráfico de dispersión de years_with_company vs. performance_score
plt.figure(figsize=(10, 6))
plt.scatter(df['years_with_company'], df['performance_score'], alpha=0.5)
plt.xlabel('Years with Company')
plt.ylabel('Performance Score')
plt.title('Dispersión de Years with Company vs. Performance Score')
plt.grid(True)
plt.show()

# Visualización 3: Gráfico de dispersión de salary vs. performance_score
plt.figure(figsize=(10, 6))
plt.scatter(df['salary'], df['performance_score'], alpha=0.5)
plt.xlabel('Salary')
plt.ylabel('Performance Score')
plt.title('Dispersión de Salary vs. Performance Score')
plt.grid(True)
plt.show()
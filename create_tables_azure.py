import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
driver = os.getenv('driver')
server = os.getenv('server')
database = os.getenv('database')
username = os.getenv('username')
password = os.getenv('password')


connection_string = (
    f'Driver={driver};'
    f'Server={server};'
    f'Database={database};'
    f'Uid={username};'
    f'Pwd={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)
# Connect to the database
try:
    conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()
    print("Connected to Azure SQL Database successfully.")

    # Load and execute the SQL script
    with open('schema.sql', 'r') as file:
        sql_script = file.read()
        cursor.execute(sql_script)
        print("SQL script executed successfully, tables created.")

    cursor.close()
    conn.close()
except Exception as e:
    print("Error connecting to database or executing script:", e)

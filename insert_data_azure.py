import pyodbc
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

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

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    print("Connected to Azure SQL Database successfully.")

except Exception as e:
    print("Error connecting to database or executing script:", e)


def load_data_to_sql(table_name, csv_file_path):
    df = pd.read_csv(csv_file_path)
    # df = df.where(pd.notnull(df), None)  # Replace NaN with None for SQL compatibility
    df.replace({np.nan: None, np.inf: None, -np.inf: None}, inplace=True)

    # Exclude identity columns for `reviews` and `sellers` tables
    if table_name == 'reviews':
        df = df.drop(columns=['review_id'])
    if table_name == 'sellers':
        df = df.drop(columns=['seller_id'])

    # Ensure proper decimal precision for specific tables
    if table_name == 'prices':
        df['price_usd'] = df['price_usd'].round(2)
        df['original_price_usd'] = df['original_price_usd'].round(2)
        df['discount_percentage'] = df['discount_percentage'].round(2)
        df['discount_amount_usd'] = df['discount_amount_usd'].round(2)
        df['shipping_cost_usd'] = df['shipping_cost_usd'].round(2)

    elif table_name == 'seller_item_performance':
        df['item_positive_feedback_percentage'] = df['item_positive_feedback_percentage'].round(2)

    for index, row in df.iterrows():
        placeholders = ', '.join(['?' for _ in row])
        columns = ', '.join(row.index)
        sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            cursor.execute(sql_query, tuple(row))
        except pyodbc.DataError as e:
            print(f"Data error with row {row} in table {table_name}: {e}")
        except pyodbc.ProgrammingError as e:
            print(f"Programming error with row {row} in table {table_name}: {e}")

    # Commit after the loop for each table
    conn.commit()
    print(f"Data loaded into {table_name} successfully.")

      
csv_folder_path = os.path.join(os.getcwd(), 'ebay_db_csv')

# Paths to the CSV files
csv_files = {
    "categories": csv_folder_path + "/categories.csv",
    "conditions": csv_folder_path + "/conditions.csv",
    "countries": csv_folder_path + "/countries.csv",
    "items": csv_folder_path + "/items.csv",
    "prices": csv_folder_path + "/prices.csv",
    "reviews": csv_folder_path + "/reviews.csv",
    "sellers": csv_folder_path + "/sellers.csv",
    "seller_item_performance": csv_folder_path + "/seller_item_performance.csv",
}

# Load each CSV file into the corresponding SQL table
for table_name, csv_path in csv_files.items():
    load_data_to_sql(table_name, csv_path)


# Close the connection
cursor.close()
conn.close()
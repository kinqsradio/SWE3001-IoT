from mysql.connector import connect, Error
from config import config
from datetime import datetime

def create_database(cursor, db_name):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        print(f"Database '{db_name}' created or already exists.")
    except Error as e:
        print(f"Error creating database {db_name}: {e}")

def create_table(cursor, device_id, sensor_data):
    table_name = f"{device_id}_Table"
    # Extracting column names and types from sensor_data
    columns = ["id INT AUTO_INCREMENT PRIMARY KEY", "DeviceID VARCHAR(255)", "Time DATETIME"]
    for key, value in sensor_data['Data'].items():
        if isinstance(value, float):
            columns.append(f"{key} FLOAT")
        elif isinstance(value, int):
            columns.append(f"{key} INT")
        elif isinstance(value, bool):
            columns.append(f"{key} BOOLEAN")
        else:
            columns.append(f"{key} VARCHAR(255)")

    create_statement = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
    cursor.execute(create_statement)
    print(f"Table '{table_name}' created or already exists.")

def retrieve_data(cursor, device_id):
    table_name = f"{device_id}_Table"
    try:
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 60")
        records = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        data_list = []
        for row in records:
            row_data = {}
            for col, val in zip(columns, row):
                if isinstance(val, datetime):
                    # Convert datetime to string
                    row_data[col] = val.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    row_data[col] = val
            data_list.append(row_data)
    except Error as e:
        print(f"Error retrieving data from {table_name}: {e}")

    return data_list
    
def get_all_device_ids(cursor):
    device_ids = []
    try:
        cursor.execute("SHOW TABLES")
        for (table_name,) in cursor:
            if table_name.endswith('_Table'):
                device_id = table_name[:-6]  # Remove '_Table' suffix to get the base device ID
                device_ids.append(device_id)
            else:
                device_ids.append(table_name)  # If not ending with '_Table', add the full table name
    except Error as e:
        print(f"Database error: {e}")
    
    
    return device_ids
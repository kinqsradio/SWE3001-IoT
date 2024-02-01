from mysql.connector import connect, Error
from dbconfig import config

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

def retrieve_sensor_data(cursor, device_id):
    table_name = f"{device_id}_Table"
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(f"Error retrieving data from {table_name}: {e}")

def get_all_device_ids():
    device_ids = []
    try:
        connection = connect(**config, database='SensorDataDB')
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        for (table_name,) in cursor:
            device_ids.append(table_name)
    except Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()
    
    return device_ids

# def create_table(cursor, table_name):
#     try:
#         cursor.execute(f"""
#             CREATE TABLE IF NOT EXISTS {table_name} (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 DHTTemperature FLOAT,
#                 Humidity FLOAT,
#                 LM35Temperature FLOAT,
#                 Time DATETIME
#             );
#         """)
#         print(f"Table '{table_name}' created or already exists.")
#     except Error as e:
#         print(f"Error creating table {table_name}: {e}")
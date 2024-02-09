from mysql.connector import connect, Error
from config import config
from datetime import datetime

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
                device_id = table_name[:-6]
                device_ids.append(device_id)
            else:
                device_ids.append(table_name)
    except Error as e:
        print(f"Database error: {e}")
    
    
    return device_ids

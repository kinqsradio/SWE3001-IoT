# from mysql.connector import Error

# def create_database(cursor, db_name):
#     try:
#         cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
#         print(f"Database '{db_name}' created or already exists.")
#     except Error as e:
#         print(f"Error creating database {db_name}: {e}")

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

from pymongo.mongo_client import MongoClient

# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://tester:TestUser2024@cluster0.hwxclzc.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
for db in client.list_databases():
    print(db)
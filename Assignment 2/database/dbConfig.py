import os
from dotenv import load_dotenv
import mysql.connector

# Load ENV File
load_dotenv()

# Set Up Config
config = {
    'user': os.getenv(key='DB_USERNAME'),
    'password': os.getenv(key='DB_PASSWORD'),
    'host': os.getenv(key='DB_HOST'),
}


# mydb = mysql.connector.connect(**config)
# print(mydb)
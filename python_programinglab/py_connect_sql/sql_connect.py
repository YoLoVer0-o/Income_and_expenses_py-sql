import mysql.connector
from mysql.connector import Error

def connectFunc():
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password="",
            database="mymoneydb",
        )
        
        if mydb.is_connected():
            print("Connected to the database")
            return mydb

    except Error as e:
        print(f"Connection Error: {e}")
        return None

import sql_connect
import pandas as pd
from mysql.connector import Error

mydb = sql_connect.connectFunc()
query = "SELECT * FROM money_list"
cursor = mydb.cursor()


def export_data():
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        df.to_csv("result_file.csv", index=False)
        print("Data exported successfully to result_file.csv")
    except Error as e:
        print(f"Error while exporting data: {e}")


def fetch_data():
    if mydb is not None:
        try:
            sql = "SELECT * FROM money_list"  # Replace 'money_list' with your actual table name
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=columns)
            print(df)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Failed to connect to the database.")


def insert_data(money_activity, date_time, money):
    try:
        sql = """
                INSERT INTO money_list (money_activity, date_time, money)
                VALUES (%s, %s, %s)
            """
        values = (money_activity, date_time, money)
        cursor.execute(sql, values)
        mydb.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error while inserting data: {e}")


def delete_data():
    try:
        delete_id = int(input("เลือกidที่จะลบ"))
        sql = "DELETE FROM money_list WHERE id = %s"
        cursor.execute(sql, (delete_id,))
        mydb.commit()
        print(f"Data deleted successfully {delete_id}")
    except Error as e:
        print(f"Error while deleting data: {e}")


def update_data():
    try:
        update_id = int(input("เลือกidที่จะเเก้ไข"))
        money_activity = str(input("เเก้ไขรายการใช้จ่าย:"))
        date_time = int(input("เเก้ไขปีเดือนวัน (YYYY-MM-DD):"))
        money = int(input("เเก้ไขจํานวนเงิน:"))
        sql = """
        UPDATE money_list
        SET money_activity = %s, date_time = %s, money = %s
        WHERE id = %s
        """
        val = (money_activity, date_time, money, update_id)
        cursor.execute(sql, val)
        mydb.commit()
    except Error as e:
        print(f"Error while update data: {e}")


def input_data():
    # if __name__ == "__main__":
    money_activity = str(input("กรอกรายการใช้จ่าย:"))
    date_time = int(input("ปีเดือนวัน (YYYY-MM-DD):"))
    money = int(input("จํานวนเงิน:"))
    print("กรอกสําเร็จ")
    insert_data(money_activity, date_time, money)


def main_menu():
    while True:
        print("\nเลือกฟังก์ชั่น:")
        print("1. ดูข้อมูลทั้งหมด")
        print("2. แปลงเป็น CSV")
        print("3. กรอกข้อมูล")
        print("4. ลบข้อมูล")
        print("5. เเก้ไขข้อมูล")
        print("6. ออก")

        choice = input("กรอกตัวเลือก: ")

        if choice == "1":
            fetch_data()
        elif choice == "2":
            export_data()
        elif choice == "3":
            input_data()
        elif choice == "4":
            delete_data()
        elif choice == "5":
            update_data()
        elif choice == "6":
            print("ออกจากระบบ...")
            cursor.close()
            mydb.close()
            break
        else:
            print("เจ๊ง.")

main_menu()

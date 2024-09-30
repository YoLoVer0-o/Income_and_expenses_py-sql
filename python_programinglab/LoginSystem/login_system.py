import json


def loginFunc():
    username = input("Enter username: ")
    password = input("Enter password: ")
    try:
        with open(
            r"C:\Learn Python\PythonProgramingLab\login\accountInfo.json", "r"
        ) as account:
            data = json.load(account)  # Load the JSON data into a Python dictionary
            for user in data:
                if user["username"] == username and user["password"] == password:
                    print("pass", username)
                    return True
                else:
                    print("username incorrect", username)
                    return False

    except FileNotFoundError:
        print("The file account_info.json was not found.")
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
    except Exception as e:
        print("An exception occurred:", e)


loginFunc()
# kjakoubec0
# mN8!KJ
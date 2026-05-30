from storage import load_data, save_data
import json
import hashlib
import os
from cryptography.fernet import Fernet
from crypto import derive_key
import base64
from hashlib import pbkdf2_hmac
from auth import register, login
from credential import add_credential, view_credentials, search_credential, delete_credential
menu = {
    1: "Register",
    2: "Login",
    3: "Add Credential",
    4: "Search Credential",
    5: "View Credentials",
    6: "Delete Credential",
    7: "Exit",
}


def display_menu():
    print("Menu:")
    for key, value in menu.items():
        print(f"{key}. {value}")


def main():
    isloggedin = False
    key_password = None
    while True:
        data = load_data()
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Register selected")
            password = input("Enter your password: ")
            key_password = register(data, password)

        elif choice == "2":
            print("Login selected")
            password = input("Enter your password: ")
            isloggedin, key_password = login(data, password)
        elif choice == "3":
            if not isloggedin:
                print("Please login first to add credentials.")
            else:
                print("Add Credential selected")
                website = input("Enter website: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                add_credential(data, key_password, website, username, password)
        elif choice == "4":
            if not isloggedin:
                print("Please login first to search credentials.")
            else:
                print("Search Credential selected")
                website = input("Enter website to search: ")
                search_credential(data, key_password, website)

        elif choice == "5":
            if not isloggedin:
                print("Please login first to view credentials.")
            else:
                print("View Credentials selected")
                view_credentials(data, key_password)

        elif choice == "6":
            if not isloggedin:
                print("Please login first to delete credentials.")
            else:
                print("Delete Credential selected")
                website = input("Enter website to delete: ")
                delete_credential(data, key_password, website)

        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")








if not os.path.exists("data.json"):
    with open("data.json", "w") as f:
        json.dump({"master_password": None, "salt": None, "credentials": {}}, f)

if __name__ == "__main__":
    main()

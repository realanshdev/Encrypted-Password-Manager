from getpass import getpass
import json
import hashlib
import os
import base64
from hashlib import pbkdf2_hmac
from cryptography.fernet import Fernet

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
        with open("data.json", "r") as f:
            data = json.load(f)
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Register selected")
            key_password = register(data)

        elif choice == "2":
            print("Login selected")
            isloggedin, key_password = login(data)
        elif choice == "3":
            if not isloggedin:
                print("Please login first to add credentials.")
            else:
                print("Add Credential selected")
                add_credential(data, key_password)
        elif choice == "4":
            if not isloggedin:
                print("Please login first to search credentials.")
            else:
                print("Search Credential selected")
                search_credential(data, key_password)

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
                delete_credential(data)

        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


def register(data):
    password = getpass("Enter your password: ")

    salt = os.urandom(16)
    data["salt"] = base64.urlsafe_b64encode(salt).decode()
    hashed = pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()
    data["master_password"] = hashed

    with open("data.json", "w") as f:
        json.dump(data, f)
    print("Registration successful!")
    return password


def login(data):
    password = getpass("Enter you password: ")
    hashed = pbkdf2_hmac(
        "sha256",
        password.encode(),
        base64.urlsafe_b64decode(data["salt"].encode()),
        100000,
    ).hex()
    if hashed == data["master_password"]:
        print("Login successful")
        return True, password
    else:
        print("Login failed. Incorrect password.")
        return False, None


def add_credential(data, key_password):
    website = input("Enter the website: ")
    username = input("Enter the username: ")
    password = getpass("Enter the password: ")
    salt = base64.urlsafe_b64decode(data["salt"].encode())
    key = derive_key(key_password, salt)
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode()).decode()

    data["credentials"][website] = {
        "username": username,
        "password": encrypted_password,
    }
    with open("data.json", "w") as f:
        json.dump(data, f)
    print("Credential added successfully!")


def search_credential(data, key_password):
    website = input("Enter the website to search: ")
    if data["credentials"].get(website):
        salt = base64.urlsafe_b64decode(data["salt"].encode())
        key = derive_key(key_password, salt)
        cipher = Fernet(key)
        decrypted_password = cipher.decrypt(
            data["credentials"][website]["password"].encode()
        ).decode()
        print(f"Username: {data['credentials'][website]['username']}")
        print(f"Password: {decrypted_password}")
    else:
        print("Credential not found.")


def view_credentials(data, key_password):
    salt = base64.urlsafe_b64decode(data["salt"].encode())
    key = derive_key(key_password, salt)
    cipher = Fernet(key)

    for website, creds in data["credentials"].items():
        decrypted_password = cipher.decrypt(creds["password"].encode()).decode()
        print(f"Website: {website}")
        print(f"Username: {creds['username']}")
        print(f"Password: {decrypted_password}")
    if not data["credentials"]:
        print("No credentials saved.")


def delete_credential(data):
    website = input("Enter the website of the credential to delete: ")
    if data["credentials"].get(website):
        del data["credentials"][website]
        with open("data.json", "w") as f:
            json.dump(data, f)
        print("Credential deleted successfully!")
    else:
        print("Credential not found.")


def derive_key(password, salt):
    key = pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return base64.urlsafe_b64encode(key)


if not os.path.exists("data.json"):
    with open("data.json", "w") as f:
        json.dump({"master_password": None, "salt": None, "credentials": {}}, f)

if __name__ == "__main__":
    main()

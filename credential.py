import base64
from hashlib import pbkdf2_hmac
from crypto import derive_key
from storage import load_data, save_data
from cryptography.fernet import Fernet
def add_credential(data, key_password, website, username, password):
    salt = base64.urlsafe_b64decode(data["salt"].encode())
    key = derive_key(key_password, salt)
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode()).decode()

    data["credentials"][website] = {
        "username": username,
        "password": encrypted_password,
    }
    save_data(data)
def view_credentials(data, key_password):
    salt = base64.urlsafe_b64decode(data["salt"].encode())
    key = derive_key(key_password, salt)
    cipher = Fernet(key)
    credentials_list = []
    for website, creds in data["credentials"].items():
        decrypted_password = cipher.decrypt(creds["password"].encode()).decode()
        credentials_list.append({"Website": website, "Username": creds["username"], "Password": decrypted_password})
    if not data["credentials"]:
        return []
    return credentials_list
def search_credential(data, key_password,website):
   
    if data["credentials"].get(website):
        salt = base64.urlsafe_b64decode(data["salt"].encode())
        key = derive_key(key_password, salt)
        cipher = Fernet(key)
        decrypted_password = cipher.decrypt(
            data["credentials"][website]["password"].encode()
        ).decode()
        return [{"Username": data['credentials'][website]['username'], "Password": decrypted_password}]
    else:
        return []

def delete_credential(data,key_password,website):
    if data["credentials"].get(website):
        del data["credentials"][website]
        save_data(data)
        print("Credential deleted successfully!")
    else:
        print("Credential not found.")




    
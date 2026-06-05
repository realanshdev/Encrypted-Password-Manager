import base64
from hashlib import pbkdf2_hmac
from crypto import derive_key
from storage import load_data, save_data
from cryptography.fernet import Fernet
from database import save_credential, get_credentials, delete_credential_db
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="password_manager",
    user="postgres",
    password="postgres"
)
def salt_():
    cursor = conn.cursor()
    cursor.execute('''SELECT salt FROM vault LIMIT 1''')
    result = cursor.fetchone()
    if not result:
        print("No user registered. Please register first.")
        return None
    else:
        salt = result[0]
        return salt
def add_credential(key_password, website, username, password):
    salt = base64.urlsafe_b64decode(salt_().encode())
    key = derive_key(key_password, salt)
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode()).decode()
    save_credential(website, username, encrypted_password)
def view_credentials(key_password):
    salt = base64.urlsafe_b64decode(salt_().encode())
    key = derive_key(key_password, salt)
    cipher = Fernet(key)
    row=get_credentials()
    credentials = []
    for _,website, username, encrypted_password in row:
        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        credentials.append({"Website": website, "Username": username, "Password": decrypted_password})
    return credentials
def search_credential(key_password,website):
   
    row=get_credentials()
    salt = base64.urlsafe_b64decode(salt_().encode())
    key = derive_key(key_password, salt)
    cipher = Fernet(key)
    for _,web, username, encrypted_password in row:
        if web == website:
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
            return {"Website": web, "Username": username, "Password": decrypted_password}
    return {"message": "Credential not found."}
def delete_credential(key_password,website):
    delete_credential_db(website)





    
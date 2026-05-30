from storage import load_data, save_data
import json
import hashlib
import os
from cryptography.fernet import Fernet
from crypto import derive_key
import base64
from hashlib import pbkdf2_hmac

def register(data,password):
    

    salt = os.urandom(16)
    data["salt"] = base64.urlsafe_b64encode(salt).decode()
    hashed = pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()
    data["master_password"] = hashed

    save_data(data)
    print("Registration successful!")
    return password


def login(data,password):
   
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

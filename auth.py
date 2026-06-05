from storage import load_data, save_data
import json
import hashlib
import os
from cryptography.fernet import Fernet
from crypto import derive_key
import base64
from hashlib import pbkdf2_hmac
from database import create_vault, init_db
import psycopg2
import psycopg2
print("Connecting to the database...")
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="password_manager",
    user="postgres",
    password="postgres"
)

def register(password):
    

    salt = os.urandom(16)
    salt1 = base64.urlsafe_b64encode(salt).decode()
    hashed = pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO vault (id,salt,master_password_hash) VALUES (%s,%s, %s) on conflict (id) DO UPDATE set salt = EXCLUDED.salt, master_password_hash = EXCLUDED.master_password_hash''', (1,salt1, hashed))
    conn.commit()
    cursor.close()
    print("Registration successful!")
    


def login(password):
    cursor = conn.cursor()
    cursor.execute('''SELECT salt, master_password_hash FROM vault LIMIT 1''')
    result = cursor.fetchone()
    if not result:
        print("No user registered. Please register first.")
        return False, None
    salt, master_password_hash = result
    hashed = pbkdf2_hmac(
        "sha256",
        password.encode(),
        base64.urlsafe_b64decode(salt.encode()),
        100000,
    ).hex()
    
    if hashed == master_password_hash:
        print("Login successful")
        return True
    else:
        print("Login failed. Incorrect password.")
        return False

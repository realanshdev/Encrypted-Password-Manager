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
from jose import  jwt
from datetime import datetime, timedelta,timezone
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException

print("Connecting to the database...")
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="password_manager",
    user="postgres",
    password="postgres"
)
SECRET_KEY = "my-super-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAuth2_obj=OAuth2PasswordBearer(tokenUrl="login")


def register(password):
    

    salt = os.urandom(16)
    salt1 = base64.urlsafe_b64encode(salt).decode()
    hashed = pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO vault (id,salt,master_password_hash) VALUES (%s,%s, %s) on conflict (id) DO UPDATE set salt = EXCLUDED.salt, master_password_hash = EXCLUDED.master_password_hash''', (1,salt1, hashed))
    conn.commit()
    cursor.close()
    print("Registration successful!")
    

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
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
        access_token = create_access_token(data={"sub": "user"})
        return  access_token
    else:
        print("Login failed. Incorrect password.")
        return  None
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None
def check_user(token:str=Depends(OAuth2_obj)):
    payload=verify_token(token)
    if payload==None:
        raise HTTPException(status_code=404,detail="User not found")
    else:
        return payload    

from fastapi import FastAPI
from pydantic import BaseModel
from auth import register,login
from storage import load_data
from credential import add_credential,view_credentials,search_credential,delete_credential
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Password Manager API!"}
class register_request(BaseModel):
    password: str
@app.post("/register")
def register_(request: register_request):
    data = load_data()
    key_password = register(data,request.password)
    return {"message": "Registration successful!"}
class login_request(BaseModel):
    password: str
isloggedin=False
@app.post("/login")
def login_(request: login_request):
    data = load_data()
    isloggedin, key_password = login(data,request.password)
    if isloggedin:
        return {"message": "Login successful!"}
    else:
        return {"message": "Login failed. Incorrect password."}
class add_credential_request(BaseModel):
    master_password: str
    website: str
    username: str
    password: str
@app.post("/add_credential")
def add_credential_(request: add_credential_request):
    data = load_data()
    add_credential(data, request.master_password, request.website, request.username, request.password)
    return {"message": "Credential added successfully!"}
@app.post("/view_credentials")
def view_credentials_(request: login_request):
    data = load_data()
    credentials = view_credentials(data, request.password)
    return credentials
class search_credential_request(BaseModel):
    password: str
    website: str
@app.post("/search_credential")
def search_credential_(request: search_credential_request):
    data = load_data()
    return search_credential(data, request.password, request.website)
class delete_credential_request(BaseModel):
    password: str
    website: str
@app.post("/delete_credential")
def delete_credential_(request: delete_credential_request):
    
    if not request.password:
        return {"message": "Password is required for authentication."}
    data = load_data()
    isloggedin,key_password = login(data,request.password)
    if(not isloggedin):
        return {"message": "Please login first to delete credentials."}
    delete_credential(data, request.password, request.website)
    return {"message": "Credential deleted successfully!"}

    
    



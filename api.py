from fastapi import FastAPI,Depends
from pydantic import BaseModel
from auth import register,login,create_access_token,verify_token,check_user
from storage import load_data
from credential import add_credential,view_credentials,search_credential,delete_credential
from database import create_vault, init_db
from fastapi.security import OAuth2PasswordRequestForm
app = FastAPI()
init_db()
create_vault()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Password Manager API!"}
class register_request(BaseModel):
    password: str
@app.post("/register")
def register_(request: register_request):
    register(request.password)
    return {"message": "Registration successful!"}
@app.post("/login")
def login_(form_data:OAuth2PasswordRequestForm=Depends()):
    token= login(form_data.password)
    if token:
        return {"access_token": token,
                "token_type": "bearer"}
    else:
        return {"message": "Login failed. Incorrect password."}
class login_request(BaseModel):
    password: str
class add_credential_request(BaseModel):
    master_password: str
    website: str
    username: str
    password: str
@app.post("/add_credential")
def add_credential_(request: add_credential_request,user=Depends(check_user)):
    add_credential(request.master_password, request.website, request.username, request.password)
    return {"message": "Credential added successfully!"}
@app.post("/view_credentials")
def view_credentials_(request:login_request ,user=Depends(check_user)):
    credentials = view_credentials(request.password)
    return credentials
class search_credential_request(BaseModel):
    password: str
    website: str
@app.post("/search_credential")
def search_credential_(request: search_credential_request,user=Depends(check_user)):
    return search_credential(request.password, request.website)
class delete_credential_request(BaseModel):
    password: str
    website: str
@app.post("/delete_credential")
def delete_credential_(request: delete_credential_request,user=Depends(check_user)):
    
    if not request.password:
        return {"message": "Password is required for authentication."}
    delete_credential(request.password, request.website)
    return {"message": "Credential deleted successfully!"}

    
    



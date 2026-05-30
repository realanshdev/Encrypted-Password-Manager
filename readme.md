# Password Manager

A secure password manager built in Python with support for both a Command Line Interface (CLI) and a FastAPI-based REST API.

## Features

* Master password authentication
* Password hashing using PBKDF2-HMAC-SHA256
* Random salt generation for enhanced security
* Credential encryption using Fernet symmetric encryption
* Store website credentials securely
* Search saved credentials
* View all stored credentials
* Delete credentials
* FastAPI REST API support
* CLI version support

## Project Structure

```text
password-manager/
├── api.py
├── cli.py
├── auth.py
├── credential.py
├── crypto.py
├── storage.py
├── README.md
```

## Security Design

### Master Password

The master password is never stored in plain text.

* Salt is generated using `os.urandom()`
* Password is hashed using PBKDF2-HMAC-SHA256
* Only the hash and salt are stored

### Credential Storage

Stored website passwords are encrypted using Fernet encryption before being saved.

This means credentials are not stored as plain text.

## API Endpoints

### Register

```http
POST /register
```

### Login

```http
POST /login
```

### Add Credential

```http
POST /add_credential
```

### View Credentials

```http
POST /view_credentials
```

### Search Credential

```http
POST /search_credential
```

### Delete Credential

```http
POST /delete_credential
```

## Technologies Used

* Python
* FastAPI
* Pydantic
* Cryptography (Fernet)
* PBKDF2-HMAC
* JSON Storage

## Future Improvements

* PostgreSQL integration
* SQLAlchemy ORM
* JWT Authentication
* Better exception handling
* Multi-user support
* Docker deployment

## Learning Outcomes

This project helped me learn:

* API development with FastAPI
* Password hashing and salting
* Symmetric encryption
* Authentication fundamentals
* Secure credential storage
* Project structuring in Python

## Author

Ansh
B.Tech CSE Student
Interested in Backend Development and Security

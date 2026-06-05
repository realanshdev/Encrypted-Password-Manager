# Encrypted Password Manager

A secure password manager built using **FastAPI**, **PostgreSQL**, and **Cryptography**.

## Features

* Master Password Registration
* Secure Login Authentication
* Password Hashing using PBKDF2-HMAC-SHA256
* Random Salt Generation
* Credential Encryption using Fernet
* Add Credentials
* View Credentials
* Search Credentials
* Delete Credentials
* PostgreSQL Database Storage
* FastAPI REST API

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* Psycopg2
* Cryptography (Fernet)
* PBKDF2-HMAC-SHA256

## Security Features

### Master Password Protection

* Master password is never stored in plain text.
* Passwords are hashed using PBKDF2-HMAC-SHA256 with 100,000 iterations.
* Unique salt is generated and stored for authentication.

### Credential Encryption

* Stored account passwords are encrypted using Fernet symmetric encryption.
* Encryption key is derived from the master password and stored salt.

## API Endpoints

### Register

POST `/register`

Registers a master password.

### Login

POST `/login`

Authenticates the user.

### Add Credential

POST `/add_credential`

Stores an encrypted credential.

### View Credentials

POST `/view_credentials`

Returns all decrypted credentials.

### Search Credential

POST `/search_credential`

Searches a credential by website.

### Delete Credential

POST `/delete_credential`

Deletes a stored credential.

## Project Evolution

### Version 1

* JSON-based storage
* Local file persistence

### Version 2

* PostgreSQL integration
* Vault table for master password storage
* Database-backed authentication
* Improved security architecture
* FastAPI endpoints for credential management

## Future Improvements

* JWT Authentication
* Multi-user support
* Update Credential API
* Password Generator
* Password Strength Checker
* Docker Deployment
* Frontend UI

## Author

Ansh


import base64
from hashlib import pbkdf2_hmac
def derive_key(password, salt):
    key = pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return base64.urlsafe_b64encode(key)
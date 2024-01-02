import os
import jwt
import bcrypt

JWT_SECRET = os.environ.get('JWT_SECRET', '<KEY>')

def authenticate(pwd: str, pwd_salt: str, token_salt: str, auth_token: str):
    print(f"pdw --> /{pwd}/ ")
    print(f"pwd_salt --> /{pwd_salt}/ ")
    print(f"token_salt --> /{token_salt}/ ")
    print(f"auth_token --> /{auth_token}/ ")
    password = pwd.encode("utf-8")
    # Hash a password for the first time, with a randomly-generated salt
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    # Check that an un-hashed password matches one that has previously been
    # hashed
    if bcrypt.checkpw(password, hashed):
        print("It Matches!")
    else:
        print("It Does not Match :(")
    return True

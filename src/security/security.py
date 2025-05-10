from flask_bcrypt import bcrypt

def hash_password(password: str) -> str:
    hashed = bcrypt.generate_password_hash(password)  
    return hashed.decode('utf-8')                    

def check_password(password: str, password_hash: str) -> bool:
    return bcrypt.check_password_hash(password_hash, password)

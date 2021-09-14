import bcrypt

def is_password_correct(login_password, password_hash):
    return bcrypt.checkpw(login_password.encode(), password_hash.encode())

def hashpw(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
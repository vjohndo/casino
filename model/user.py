from model.database import sql_select, sql_write

def user_exists_of_email(email):
    fetched_items = sql_select("SELECT id FROM users WHERE email = %s", [email])
    return bool(len(fetched_items))

def name_of_id(id):
    return sql_select("SELECT name FROM users WHERE id = %s", [id])[0][0]

def user_profile_of_email(email):
    databse_result = sql_select("SELECT id, name, email, password_hash FROM users WHERE email = %s", [email])
    
    return {'id': databse_result[0][0],
            'name': databse_result[0][1],
            'email': databse_result[0][2],
            'password_hash': databse_result[0][3]}

def user_profile_of_id(id):
    databse_result = sql_select("SELECT id, name, email, password_hash FROM users WHERE id = %s", [id])
    
    return {'id': databse_result[0][0],
            'name': databse_result[0][1],
            'email': databse_result[0][2],
            'password_hash': databse_result[0][3]}

def add_user(email, name, password_hash):
    sql_write("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",[email, name, password_hash])
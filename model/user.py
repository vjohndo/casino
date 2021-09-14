from model.database import sql_select, sql_write
from model.player import Player

def user_exists_of_email(email):
    fetched_items = sql_select("SELECT id FROM users WHERE email = %s", [email])
    return bool(len(fetched_items))

def user_profile_of_email(email):
    databse_result = sql_select("SELECT id, name, email, password_hash, wallet, is_admin, last_login FROM users WHERE email = %s", [email])
    
    return Player(databse_result[0][0], databse_result[0][1], databse_result[0][2], databse_result[0][3], databse_result[0][4], databse_result[0][4])

def user_profile_of_id(id):
    databse_result = sql_select("SELECT id, name, email, password_hash, wallet, is_admin, last_login FROM users WHERE id = %s", [id])
    
    # Get out a class of the player
    return Player(databse_result[0][0], databse_result[0][1], databse_result[0][2], databse_result[0][3], databse_result[0][4], databse_result[0][4])

def add_user(email, name, password_hash):
    sql_write("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",[email, name, password_hash])


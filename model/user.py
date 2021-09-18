from model.database import sql_select, sql_write
from model.player import Player
from datetime import date

# Given an email, checks if a user exists
def user_exists_of_email(email):
    fetched_items = sql_select("SELECT id FROM users WHERE email = %s", [email])
    return bool(len(fetched_items))

# Given an email, returns a player class
def user_profile_of_email(email):
    databse_result = sql_select("SELECT id, name, email, password_hash, wallet, is_admin, last_login FROM users WHERE email = %s", [email])
    
    return Player(databse_result[0][0], databse_result[0][1], databse_result[0][2], databse_result[0][3], databse_result[0][4], databse_result[0][5], databse_result[0][6])

# Given an ID, returns player class
def user_profile_of_id(id):
    databse_result = sql_select("SELECT id, name, email, password_hash, wallet, is_admin, last_login FROM users WHERE id = %s", [id])
    
    return Player(databse_result[0][0], databse_result[0][1], databse_result[0][2], databse_result[0][3], databse_result[0][4], databse_result[0][5], databse_result[0][6])

# Takes user inputs from sign up to generate new row in database
def add_user(email, name, password_hash):
    sql_write("INSERT INTO users (email, name, password_hash, wallet, last_login) VALUES (%s, %s, %s, %s, %s)",[email, name, password_hash, 0, date(1900,1,1) ])

# Takes player class and uses those values to update
def update_player(player):
    sql_write(
        "UPDATE users SET wallet = %s, last_login = %s WHERE id = %s",
        [player.wallet, player.last_login ,player.id]
    )
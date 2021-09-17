from model.database import sql_select, sql_write
import pickle 

# Game id --> game_mode_id
# played_games --> game_instances

def create_gamedb(game_instance):

    pickled_game = pickle.dumps(game_instance)

    sql_write(
        "INSERT INTO game_instances (user_id, game_mode_id, bet_amount, pickled_game, game_over, result) VALUES (%s, %s, %s, %s, %s, %s)",
        [game_instance.player_id, game_instance.game_mode_id, game_instance.bet_amount, pickled_game, False, 0]
    )

def update_gamedb(game_instance):

    pickled_game = pickle.dumps(game_instance)

    sql_write(
        "UPDATE game_instances SET pickled_game = %s, bet_amount = %s , game_over = %s, result = %s WHERE id = %s",
        [pickled_game, game_instance.bet_amount ,game_instance.is_over, game_instance.payout_amount ,game_instance.game_instance_id]
    )

def read_gamedb(played_game_id):
    
    pickled_game = sql_select("SELECT pickled_game FROM game_instances WHERE id = %s",[played_game_id])[0][0]
    unpickled_game = pickle.loads(pickled_game)
    unpickled_game.game_instance_id = played_game_id

    return unpickled_game

def any_active_gamedb(user_id, game_mode_id):

    return bool(sql_select("SELECT pickled_game FROM game_instances WHERE user_id = %s AND game_over = %s AND game_mode_id = %s",[user_id, False, game_mode_id]))


def get_pokerID_by_userID(user_id):

    return sql_select("SELECT id FROM game_instances WHERE user_id = %s AND game_over = %s",[user_id, False])[0][0]

def get_pokerID_by_userID(user_id):

    return sql_select("SELECT id FROM game_instances WHERE user_id = %s AND game_over = %s AND game_mode_id = %s",[user_id, False, 1])[0][0]

def get_blackjackID_by_userID(user_id):

    return sql_select("SELECT id FROM game_instances WHERE user_id = %s AND game_over = %s AND game_mode_id = %s",[user_id, False, 2])[0][0]
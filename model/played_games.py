from model.database import sql_select, sql_write
import pickle 

def create_gamedb(game_instance):

    pickled_game = pickle.dumps(game_instance)

    sql_write(
        "INSERT INTO played_games (user_id, game_id, bet_amount, pickled_game, game_over, result) VALUES (%s, %s, %s, %s, %s, %s)",
        [game_instance.player_id, 1, game_instance.bet_amount, pickled_game, False, 0]
    )

def update_gamedb(game_instance):

    pickled_game = pickle.dumps(game_instance)

    sql_write(
        "UPDATE played_games SET pickled_game = %s, game_over = %s, result = %s WHERE id = %s",
        [pickled_game, game_instance.is_over, game_instance.payout_amount ,game_instance.game_instance_id]
    )

def read_gamedb(played_game_id):
    
    pickled_game = sql_select("SELECT pickled_game FROM played_games WHERE id = %s",[played_game_id])[0][0]
    unpickled_game = pickle.loads(pickled_game)
    unpickled_game.game_instance_id = played_game_id

    return unpickled_game

def any_active_gamedb(user_id):

    return bool(sql_select("SELECT pickled_game FROM played_games WHERE user_id = %s AND game_over = %s",[user_id, False]))


def get_gameID_by_userID(user_id):

    return sql_select("SELECT id FROM played_games WHERE user_id = %s AND game_over = %s",[user_id, False])[0][0]
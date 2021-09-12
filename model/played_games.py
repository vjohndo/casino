from model.database import sql_select, sql_write
import pickle 

def add_game(game_instance):

    pickled_game = pickle.dumps(game_instance)

    sql_write(
        "INSERT INTO played_games (user_id, game_id, bet_amount, pickled_game, game_over, result) VALUES (%s, %s, %s, %s, %s, %s)",
        [game_instance.player.id, 1, game_instance.bet_amount, pickled_game, False, 0]
    )

def update_game(game_instance, game_id):

    pickled_game = pickle.dumps(game_instance)

    sql_write(
        "UPDATE played_games SET pickled_game = %s WHERE id = %s",
        [pickled_game, game_id]
    )



def load_game(played_game_id):
    
    pickled_game = sql_select("SELECT pickled_game FROM played_games WHERE id = %s",[played_game_id])[0][0]
    unpickled_game = pickle.loads(pickled_game)

    return unpickled_game

from model.played_games import create_game
from flask import Flask, render_template, request, redirect, session
import bcrypt
import pickle

from model.five_card_draw import Five_Card_Draw
from model.player import Player
from model.user import *
from model.played_games import create_game, read_game, update_game

app = Flask(__name__)


# Want to serve a unique instance of a teh game to the use and keep track of it
# Will eventually need to pickle the game to throw it in the DB 
# https://stackoverflow.com/questions/57642165/saving-python-object-in-postgres-table-with-pickle
# test_player = Player(1, 'John', 'john.do@email.com', 5000)
# game = Five_Card_Draw(test_player,100)
# pickle_string = pickle.dumps(game)

app.config['SECRET_KEY'] = 'ThisKeyTesting'


# @app.route('/create_game')
# def create_game():

#     # Get a player class
#     test_player = Player(1, 'John', 'john.do@email.com', 5000)

#     temp_game = Five_Card_Draw()
#     create_game()

#     return redirect("/")
#     """ 
#     Need to create a route to create the game 
#     """

@app.route('/')
def index():

    """ 
    Route to direct to landing page rather than an active version of the game
    Need to create proper player class before doing this. 
    """

    if session.get('user_id') is None: 
        return render_template('index.jinja', hand = enumerate(hand))
    else:
        name = name_of_id(session.get('user_id'))
        # Create an instance of the player object & Game
        loaded_game = read_game(1)
        game = loaded_game
        
        # test_player = Player(session.get('user_id'), 'John', 'john.do@email.com', 5000)
        # game = Five_Card_Draw(test_player,100)
        hand = game.get_hand()
        update_game(game,1)

        # Check if there an existing game in the database that is incomplete

        return render_template('index.jinja', hand = enumerate(hand), name=name)

@app.route('/action', methods = ['POST'])
def action():

    loaded_game = read_game(1)
    game = loaded_game
    form_request = list(request.form)
    game.redraw(form_request)
    print("FORM REQUEST",form_request)
    update_game(game,1)
    return redirect('/')

# LOGIN #
@app.route("/login")
def login():
    if session.get('user_id'):
        return redirect('/')

    fields_empty = False
    wrong_details = False

    if session.get('fields_empty'):
        fields_empty = True

    if session.get('wrong_details'): 
        wrong_details = True

    return render_template("login.jinja", fields_empty=fields_empty, wrong_details = wrong_details)

@app.route("/login_action", methods=["POST"])
def login_action():
    if session.get('user_id'):
        return redirect('/')

    login_email = request.form.get("username")
    login_password = request.form.get("password")
    session['fields_empty'] = False
    session['wrong_details'] = False

    if 0 in [len(x) for x in [login_email, login_password]]:
        session['fields_empty'] = True
        return redirect('/login') 

    if user_exists_of_email(login_email):
        user_profile = user_profile_of_email(login_email)
        password_hash = user_profile['password_hash']
        password_is_valid = bcrypt.checkpw(login_password.encode(), password_hash.encode())
        
        if password_is_valid:
            session['user_id'] = user_profile['id']
            return redirect("/")
        
    session['wrong_details'] = True
    return redirect("/login")
        
# SIGN UP
@app.route('/signup')
def sign_up():
    email_already_exists = False
    passwords_not_match = False
    fields_empty = False
    
    if session.get('user_id'):
        return redirect('/')

    if session.get('already_exists'):
        email_already_exists = True
    
    if session.get('passwords_not_match'):
        passwords_not_match = True

    if session.get('fields_empty'):
        fields_empty = True
    
    return render_template('signup.jinja', already_exists = email_already_exists, passwords_not_match = passwords_not_match, fields_empty = fields_empty)

@app.route('/signup_action', methods=['POST'])
def signup_action():
    signup_email = request.form.get('email')
    signup_name = request.form.get('name')
    signup_password1 = request.form.get('password1')
    signup_password2 = request.form.get('password2')

    session['already_exists'] = None
    session['passwords_not_match'] = None

    if 0 in [len(x) for x in [signup_email, signup_email, signup_password1, signup_password2]]:
        session['fields_empty'] = True
        return redirect('/signup') 

    if user_exists_of_email(signup_email):
        session['already_exists'] = True
        return redirect('/signup') 
    
    if signup_password1 != signup_password2:
        session['passwords_not_match'] = True
        return redirect('/signup') 

    password_hash = bcrypt.hashpw(signup_password1.encode(), bcrypt.gensalt()).decode()
    add_user(signup_email,signup_name,password_hash)
    session['user_id'] = user_profile_of_email(signup_email)['id']
    return redirect("/")

# LOGOUT #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/sort', methods = ['POST'])
def sort():
    
    loaded_game = read_game(1)
    game = loaded_game
    game.hand_sort()
    update_game(game,1)

    return redirect('/')

@app.route('/checkwin', methods = ['POST'])
def checkwin():
    loaded_game = read_game(1)
    game = loaded_game
    game.bet = int(request.form.get('bet'))
    hand = game.get_hand()
    result_tuple = game.payout()
    update_game(game,1)
    return render_template('index.jinja', hand = enumerate(hand), game_case = result_tuple[0], payout = result_tuple[1])

if __name__ == '__main__':
    app.run(debug=True)
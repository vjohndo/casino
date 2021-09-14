from model.played_games import any_active_gamedb, create_gamedb, get_gameID_by_userID
from flask import Flask, render_template, request, redirect, session
import bcrypt
import pickle


from model.encryption import is_password_correct
from model.five_card_draw import Five_Card_Draw
from model.player import Player
from model.user import *
from model.played_games import create_gamedb, read_gamedb, update_gamedb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisKeyTesting'

@app.route('/create_game')
def create_game():

    # Get a player class
    player = user_profile_of_id(session.get('user_id'))
    
    # Create an instance of the game 
    game_init = Five_Card_Draw(player.id)

    # Create an entry of the game in the database
    create_gamedb(game_init)

    return redirect("/")

@app.route('/play_game')
def play_game():

    # Get a player class
    player = user_profile_of_id(session.get('user_id'))

    # Check if there are any active games
    if any_active_gamedb(player.id):
        
        # Open up that active game
        game_id = get_gameID_by_userID(player.id)
        game = read_gamedb(game_id)
        print(game.hand[0])
        update_gamedb(game)
    
    return render_template("play_game.jinja", name = player.name, enumerated_hand = enumerate(game.hand))


@app.route('/')
def index():

    """ 
    Route to direct to landing page rather than an active version of the game
    Need to create proper player class before doing this. 
    """

    if session.get('user_id') is None: 
        return render_template('index.jinja')
    else:

        # Create an instance of the player
        user_profile = user_profile_of_id(session.get('user_id'))

        # if any_active_game(user_profile.id):


        # Check if any instance of a game exists 



        # # Create an instance of the player object & Game
        # loaded_game = read_game(1)
        # game = loaded_game
        
        # # test_player = Player(session.get('user_id'), 'John', 'john.do@email.com', 5000)
        # # game = Five_Card_Draw(test_player,100)
        # hand = game.get_hand()
        # update_game(game,1)

        # Check if there an existing game in the database that is incomplete

        return render_template('index.jinja', name=user_profile.name)

@app.route('/action', methods = ['POST'])
def action():

    loaded_game = read_gamedb(1)
    game = loaded_game
    form_request = list(request.form)
    game.redraw(form_request)
    print("FORM REQUEST",form_request)
    update_gamedb(game,1)
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

    # Need to update with player class
    if user_exists_of_email(login_email):
        user_profile = user_profile_of_email(login_email)
        password_hash = user_profile.passwordHash
        
        if is_password_correct(login_password, password_hash):
            session['user_id'] = user_profile.id
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
    
    loaded_game = read_gamedb(1)
    game = loaded_game
    game.hand_sort()
    update_gamedb(game,1)

    return redirect('/')

@app.route('/checkwin', methods = ['POST'])
def checkwin():
    loaded_game = read_gamedb(1)
    game = loaded_game
    game.bet = int(request.form.get('bet'))
    hand = game.get_hand()
    result_tuple = game.payout()
    update_gamedb(game,1)
    return render_template('index.jinja', hand = enumerate(hand), game_case = result_tuple[0], payout = result_tuple[1])

if __name__ == '__main__':
    app.run(debug=True)
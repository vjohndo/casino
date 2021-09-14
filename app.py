from model.played_games import any_active_gamedb, create_gamedb, get_gameID_by_userID
from flask import Flask, render_template, request, redirect, session

from model.encryption import is_password_correct, hashpw
from model.five_card_draw import Five_Card_Draw
from model.user import user_exists_of_email, user_profile_of_id, user_profile_of_email, add_user
from model.played_games import create_gamedb, read_gamedb, update_gamedb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisKeyTesting'

# LANDING PAGE
@app.route('/')
def index():
    if session.get('user_id') is None: 
        return render_template('index.jinja')

    else:
        user_profile = user_profile_of_id(session.get('user_id'))
        return render_template('index.jinja', name=user_profile.name)

# FIVE CARD POKER
@app.route('/create_game')
def create_game():

    # Get a player class
    player = user_profile_of_id(session.get('user_id'))
    
    # Create an instance of the game 
    game_init = Five_Card_Draw(player.id)

    # Create an entry of the game in the database
    create_gamedb(game_init)

    return redirect("/play_game")

@app.route('/play_game')
def play_game():

    # Get a player class
    player = user_profile_of_id(session.get('user_id'))

    # Check if there are any active games
    if any_active_gamedb(player.id):
        
        # Open up that active game
        game_id = get_gameID_by_userID(player.id)
        session['game_instance_id'] = game_id
        game = read_gamedb(game_id)
        update_gamedb(game)
    
    return render_template("play_game.jinja", name = player.name, enumerated_hand = enumerate(game.hand))

@app.route('/game_redraw', methods = ['POST'])
def action():

    game_id = session.get('game_instance_id')
    game = read_gamedb(game_id)
    form_request = list(request.form)
    print(form_request)
    game.redraw(form_request)
    update_gamedb(game)

    return redirect('/play_game')

@app.route('/game_sort', methods = ['POST'])
def sort():
    
    game_id = session.get('game_instance_id')
    game = read_gamedb(game_id)
    game.hand_sort()
    update_gamedb(game)

    return redirect('/play_game')

@app.route('/checkwin', methods = ['POST'])
def checkwin():

    game_id = session.get('game_instance_id')
    game = read_gamedb(game_id)
    game.bet = int(request.form.get('bet'))
    result_tuple = game.payout()
    update_gamedb(game)

    return render_template('play_game.jinja', enumerated_hand = enumerate(game.hand), game_case = result_tuple[0], payout = result_tuple[1])

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

    password_hash = hashpw(signup_password1)
    add_user(signup_email,signup_name,password_hash)
    session['user_id'] = user_profile_of_email(signup_email).id
    return redirect("/")

# LOGOUT #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
from model.dailycheck import moreThanADay
from model.played_games import any_active_gamedb, create_gamedb, get_pokerID_by_userID, get_blackjackID_by_userID
from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta, date
from model.dailycheck import moreThanADay
import os

from model.encryption import is_password_correct, hashpw
from model.five_card_draw import Five_Card_Draw
from model.blackjack import Blackjack
from model.user import user_exists_of_email, user_profile_of_id, user_profile_of_email, add_user, update_player
from model.played_games import create_gamedb, read_gamedb, update_gamedb



SECRET_KEY = os.environ.get("SECRET_KEY", 'ThisKeyTesting')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Money Collection
@app.route('/collect')
def collect_daily():
    # Get a player class
    player = user_profile_of_id(session.get('user_id'))

    if moreThanADay(player):
        player.last_login = date.today()
        player.wallet += 100
        update_player(player)
        return redirect('/')
    else:
        return redirect('/')

# LANDING PAGE
@app.route('/')
def index():
    if session.get('user_id') is None: 
        return render_template('index.jinja')

    else:
        try:
            user_profile = user_profile_of_id(session.get('user_id'))
            can_collect = moreThanADay(user_profile)
        except:
            session.clear()
            return redirect('/login')
        return render_template('index.jinja', name=user_profile.name, wallet=user_profile.wallet, can_collect=can_collect)

# BLACK JACK
@app.route('/create_game_blackjack', methods=['GET'])
def create_game_blackjack():

    # Get a player class
    player = user_profile_of_id(session.get('user_id'))

    # Create an instance of the blackjack game
    if not any_active_gamedb(player.id,2):
            
        game_init = Blackjack(player.id)
        create_gamedb(game_init)

    # Create an entry of the game in the database
    return redirect('/bet_game_blackjack')

@app.route('/bet_game_blackjack')
def blackjack_place_bet():

    if session.get('user_id') is not None: 

        # Get the player class
        player = user_profile_of_id(session.get('user_id'))

        # Any active games for this player, including those just created?
        if any_active_gamedb(player.id,2):
            
            # Load game from player ID
            game_id = get_blackjackID_by_userID(player.id)
            session['game_instance_id_blackjack'] = game_id
            game = read_gamedb(game_id)

            # Of those active games, has bet been placed?
            if game.bet_placed == True:
                return redirect('/play_game_blackjack')
            else:
                return render_template(
                                'bet_blackjack.jinja',
                                name = player.name,
                                enumerated_hand = enumerate(game.player_hand),
                                wallet=player.wallet,
                                game_instance = game.game_instance_id
                )
        
        # No active game
        else:
            return redirect('/create_game_blackjack')

    else:
        return redirect('/login')

@app.route('/play_game_blackjack', methods=['POST','GET'])
def play_game_blackjack():

    # open up the game
    player = user_profile_of_id(session.get('user_id'))
    game_id = get_blackjackID_by_userID(player.id)
    session['game_instance_id_blackjack'] = game_id
    game = read_gamedb(game_id)

    # update the bet amount if the gmae still hasn't been updated
    if game.bet_placed == False:
        
        if not request.form.get('bet_value'):
            return redirect('/bet_game')

        game.bet_amount = int(request.form.get('bet_value'))

        if game.bet_amount < 1 or game.bet_amount > player.wallet:
            return redirect('/bet_game_blackjack')

        player.wallet = player.wallet - game.bet_amount
        update_player(player)
        game.bet_placed = True
        update_gamedb(game)
    
    no_hits = False

    if game.player_bust == True or game.player_blackjack == True:
        no_hits = True 
    
    return render_template(
                    "play_game_blackjack.jinja",
                    game = game, 
                    no_hits = no_hits, 
                    name = player.name, 
                    dealer_hand = enumerate(game.dealer_hand), 
                    enumerated_hand = enumerate(game.player_hand), 
                    wallet=player.wallet, bet_amount=game.bet_amount, 
                    game_instance = game.game_instance_id
    )


@app.route('/blackjack_hit', methods=['POST'])
def blackjack_hit():
    game_id = session.get('game_instance_id_blackjack')
    game = read_gamedb(game_id)
    game.hit()
    update_gamedb(game)
    return redirect('/play_game_blackjack')

@app.route('/blackjack_stay', methods=['POST'])
def blackjack_stay():

    game_id = session.get('game_instance_id_blackjack')
    game = read_gamedb(game_id)
    game.dealer_plays()
    update_gamedb(game)
    return redirect('/checkwin_blackjack')


@app.route('/checkwin_blackjack', methods=['POST','GET'])
def checkwin_blackjack():
    player = user_profile_of_id(session.get('user_id'))
    game_id = session.get('game_instance_id_blackjack')
    game = read_gamedb(game_id)
    no_hits = False

    if game.is_over:
        return render_template(
                        "play_game_blackjack.jinja", 
                        game=game , 
                        game_over = game.is_over, 
                        no_hits = no_hits, name = player.name, 
                        dealer_hand = enumerate(game.dealer_hand), 
                        enumerated_hand = enumerate(game.player_hand), 
                        wallet=player.wallet, bet_amount=game.bet_amount, 
                        game_instance = game.game_instance_id
        )

    else:
        player.wallet = player.wallet + game.payout_amount
        game.results()
        update_gamedb(game)
        update_player(player)

        return render_template(
                        "play_game_blackjack.jinja", 
                        game=game , 
                        game_over = game.is_over, 
                        no_hits = no_hits, name = player.name, 
                        dealer_hand = enumerate(game.dealer_hand), 
                        enumerated_hand = enumerate(game.player_hand), 
                        wallet=player.wallet, bet_amount=game.bet_amount, 
                        game_instance = game.game_instance_id
        )


# FIVE CARD POKER
@app.route('/create_game', methods=['GET'])
def create_game():
    if session.get('user_id') is not None: 

        # Get a player class
        player = user_profile_of_id(session.get('user_id'))
        
        # Create ab instance of the game only is not other active game.
        if not any_active_gamedb(player.id,1):
            
            # Create an instance of the game 
            game_init = Five_Card_Draw(player.id)
            create_gamedb(game_init)

        return redirect("/bet_game")

    else:
        return redirect('/login')

# BET # THIS IS THE PROBLEM ONE. 
@app.route('/bet_game')
def poker_place_bet():

    if session.get('user_id') is not None: 

            # Get a player class
            player = user_profile_of_id(session.get('user_id'))    

            # Check if there are any active games, that are not finished
            if any_active_gamedb(player.id, 1):

                # Open up that game we just created
                game_id = get_pokerID_by_userID(player.id)
                session['game_instance_id'] = game_id
                game = read_gamedb(game_id)
                
                # If that active game has had its bet placed, direct to play games
                if game.bet_placed == True:
                    return redirect('/play_game')
                
                # Otherwise we've not yet placed bet
                else:
                    return render_template(
                                'bet.jinja',
                                name = player.name,
                                enumerated_hand = enumerate(game.hand), 
                                wallet=player.wallet, 
                                game_instance = game.game_instance_id
                    )
            
            # No active game? then create one.
            else:
                return redirect('/create_game')
        
    else:
        return redirect('/login')
    

@app.route('/play_game', methods=['POST','GET'])
def play_game():

    # Open up the game
    player = user_profile_of_id(session.get('user_id'))
    game_id = get_pokerID_by_userID(player.id)
    session['game_instance_id'] = game_id
    game = read_gamedb(game_id)
    
    # update the bet amount it has not been updated.
    if game.bet_placed == False:

        if not request.form.get('bet_value'):
            return redirect('/bet_game')

        if game.bet_amount < 1 or game.bet_amount > player.wallet:
            return redirect('/bet_game')

        player.wallet = player.wallet - game.bet_amount
        update_player(player)
        game.bet_placed = True
        update_gamedb(game)
        
    return render_template(
                    "play_game.jinja", 
                    name = player.name, 
                    enumerated_hand = enumerate(game.hand), 
                    wallet=player.wallet, 
                    bet_amount=game.bet_amount, 
                    game_instance = game.game_instance_id
    )
    
    
@app.route('/game_redraw', methods = ['POST'])
def action():

    game_id = session.get('game_instance_id')
    game = read_gamedb(game_id)
    form_request = list(request.form)
    if form_request:
        game.redraw(form_request)
        update_gamedb(game)
    return redirect('/checkwin')

@app.route('/game_sort', methods = ['POST'])
def sort():
    
    game_id = session.get('game_instance_id')
    game = read_gamedb(game_id)
    game.hand_sort()
    update_gamedb(game)
    return redirect('/play_game')

@app.route('/checkwin', methods = ['POST','GET'])
def checkwin():
    # Get a player class
    player = user_profile_of_id(session.get('user_id'))
    game_id = session.get('game_instance_id')
    game = read_gamedb(game_id)
    print('GAME IS OVER?', game.is_over)

    if game.is_over == False:
        print('if statement')
        game.payout()
        player.wallet = player.wallet + game.payout_amount
        update_player(player)
        update_gamedb(game)
        return render_template(
                        'play_game.jinja',
                        name = player.name, 
                        wallet=player.wallet, 
                        enumerated_hand = enumerate(game.hand), 
                        game_case = game.winning_case, 
                        payout = game.payout_amount, 
                        bet_amount=game.bet_amount, 
                        game_instance = game.game_instance_id
        )
    else:
        print('Else statement')
        return render_template(
                        'play_game.jinja',
                        name = player.name, 
                        wallet=player.wallet, 
                        enumerated_hand = enumerate(game.hand), 
                        game_case = game.winning_case, 
                        payout = game.payout_amount, 
                        bet_amount=game.bet_amount, 
                        game_instance = game.game_instance_id
        )

### LOGIN ###
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
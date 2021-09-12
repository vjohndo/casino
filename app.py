from flask import Flask, render_template, request, redirect
from model.five_card_draw import Five_Card_Draw
from model.player import Player

app = Flask(__name__)

# Will eventually need to pickle the game to throw it in the DB 
# https://stackoverflow.com/questions/57642165/saving-python-object-in-postgres-table-with-pickle
test_player = Player(1, 'John', 'john.do@email.com', 5000)
game = Five_Card_Draw(test_player,100)

# Want to be able to interact with the game now
@app.route('/')
def index():
    
    hand = game.get_hand()
    return render_template('index.jinja', hand = enumerate(hand))

@app.route('/action', methods = ['POST'])
def action():
    form_request = list(request.form)
    game.redraw(form_request)
    print("FORM REQUEST",form_request)
    return redirect('/')

@app.route('/sort', methods = ['POST'])
def sort():
    game.hand_sort()
    return redirect('/')

@app.route('/checkwin', methods = ['POST'])
def checkwin():
    game.bet = int(request.form.get('bet'))
    hand = game.get_hand()
    result_tuple = game.payout()
    return render_template('index.jinja', hand = enumerate(hand), game_case = result_tuple[0], payout = result_tuple[1])

if __name__ == '__main__':
    app.run(debug=True)
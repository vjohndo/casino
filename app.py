from flask import Flask, render_template
from model.five_card_draw import Five_Card_Draw
from model.player import Player

app = Flask(__name__)

test_player = Player(1, 'John', 'john.do@email.com', 5000)
game = Five_Card_Draw(test_player,100)

@app.route('/')
def index():
    
    hand = game.get_hand()
    return render_template('index.jinja', hand = hand)

if __name__ == '__main__':
    app.run(debug=True)
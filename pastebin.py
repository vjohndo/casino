# Get data
@app.route('/getName')
def retrieve_data():
    print("in getName view")
    output = {"name": 'THE TEST NAME WORKS'}
    return jsonify(output)  

# Get hand
@app.route('/getHand')
def get_hand():

    # Get a player class
    player = user_profile_of_id(session.get('user_id'))

    if any_active_gamedb(player.id):
        
        # Open up that active game
        game_id = get_gameID_by_userID(player.id)
        session['game_instance_id'] = game_id
        game = read_gamedb(game_id)
        hand = game.hand
        update_gamedb(game)
        return jsonify(hand)
    else:
        return redirect('/create_game')



const title = document.getElementById("testingAsync")

// Request arbitray info form server. 
const getName = async () => {
    try {
        const response = await fetch('/getHand');
        const resp = await response.json();
        console.log("Obj returned from server", resp);
    } catch (error) {
        console.log('Fetch error: ', error);
    }
}

title.addEventListener('click', getName)


const gameboard = document.getElementById('display')
const getHand = async () => {
    try {
        const response = await fetch('/getName');
        const resp = await response.json();
        console.log("Obj returned from server", resp);
    } catch (error) {
        console.log('Fetch error: ', error);
    }
}
const fiveCardPokerButton = document.querySelector("#fiveCardPokerButton") 
const blackjackButon = document.querySelector("#blackjackButton")

fiveCardPokerButton.onclick = function() {
    window.location.replace("/bet_game")
}

blackjackButon.onclick = function() {
    window.location.replace("/create_game_blackjack")
}

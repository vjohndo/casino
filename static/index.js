// This script adds in functionality to collect reroute buttons
const fiveCardPokerButton = document.querySelector("#fiveCardPokerButton") 
const blackjackButon = document.querySelector("#blackjackButton")
const collectDaily = document.querySelector("#moneyCollect")

fiveCardPokerButton.onclick = function() {
    window.location.replace("/bet_game")
}

blackjackButon.onclick = function() {
    window.location.replace("/create_game_blackjack")
}

if (collectDaily) {
    collectDaily.onclick = function() {
        window.location.replace("/collect")
    }
}
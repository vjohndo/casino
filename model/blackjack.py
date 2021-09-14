from player import Player
from deck import Deck

class Blackjack():

    def __init__(self, player_id, bet_amount = 10):
        self.game_instance_id = None
        self.game_over = False
        self.payout_amount = None
        self.player_id = player_id
        self.bet_amount = bet_amount
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0

        # Deal to dealer_
        for i in range(2):
            self.player_hand.append(self.deck.deal())
            self.dealer_hand.append(self.deck.deal())


    # Need a way to evaluate the total of hand
    def score_hand(self):
        hand_as_values = [card.blackjack_value for card in self.player_hand]

        # Need to keep reducing all Aces in hand 



    ## Will need to account for the dealers and players blackjacl
    def dealer(self):
        pass

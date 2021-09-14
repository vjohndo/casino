from player import Player
from deck import Deck, Card

class Blackjack():

    def __init__(self, player_id, bet_amount = 10):
        self.game_instance_id = None
        self.game_over = False
        self.result = None
        self.payout_amount = None
        self.player_id = player_id
        self.bet_amount = bet_amount
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.player_blackjack = False
        self.dealer_blackjack = False
        self.player_bust = False
        self.dealer_bust = False

        # Deal to dealer_
        for i in range(2):
            self.player_hand.append(self.deck.deal())
            self.dealer_hand.append(self.deck.deal())

        # Check for blackjacks
        self.score_dealer_hand()
        self.score_player_hand()

        if self.player_score == 21:
            self.player_blackjack = True
        
        if self.dealer_score == 21:
            self.dealer_blackjack = True

    # Need a way to evaluate the total of hand
    def score_player_hand(self):
        hand_as_values = [card.blackjack_value for card in self.player_hand]

        # Need to keep reducing all Aces in hand should your total value be above 21
        while sum(hand_as_values) > 21 and 11 in hand_as_values:
            hand_as_values[hand_as_values.index(11)] = 1
        
        # Update the players score
        self.player_score = sum(hand_as_values)
        if self.player_score > 21:
            self.player_bust = True
            self.player_score = 0


    def score_dealer_hand(self):
        hand_as_values = [card.blackjack_value for card in self.dealer_hand]

        # Need to keep reducing all Aces in hand should your total value be above 21
        while sum(hand_as_values) > 21 and 11 in hand_as_values:
            hand_as_values[hand_as_values.index(11)] = 1
        
        # Update the players score
        self.dealer_score = sum(hand_as_values)
        if self.dealer_score > 21:
            self.dealer_bust = True
            self.dealer_score = 0


    ## Will need to account for the dealers and players blackjacl
    def takes(self):
        self.dealer_hand.append(self.deck.deal())
        self.score_dealer_hand()

    
    def hit(self):
        self.player_hand.append(self.deck.deal())
        self.score_player_hand()

    def dealer_plays(self):
        
        while self.dealer_score < 17 and not self.dealer_bust:
            self.takes()
            self.score_dealer_hand()

    # This is to compare the results
    def results(self):

        # Check all blackjack conditions

        if self.player_blackjack and self.dealer_blackjack:
            self.result = 'DRAW'
            self.payout_amount = self.bet_amount

        elif self.player_blackjack and not self.dealer_blackjack:
            self.result = "Player's Blackjack"
            self.payout_amount = self.bet_amount * 2.5
        
        elif not self.player_blackjack and self.dealer_blackjack:
            self.result = "Dealers's Blackjack"
            self.payout_amount = 0

        # Compare scores
        else:
            if self.player_score == self.dealer_score:
                self.result = 'DRAW'
                self.payout_amount = self.bet_amount

            elif self.player_score > self.dealer_score:
                self.result = "Player Wins"
                self.payout_amount = self.bet_amount * 2
            
            elif not self.player_score < self.dealer_score:
                self.result = "Dealers Wins"
                self.payout_amount = 0
            

        # Set game to finished
        self.game_over = True

    def get_hands(self):
        print('PLAYERS HAND: ',self.player_hand)
        print('DEALERS HAND: ',self.dealer_hand)


test = Blackjack(1)
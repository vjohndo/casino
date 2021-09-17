from model.player import Player
from model.deck import Deck, Card

class Blackjack():

    def __init__(self, player_id):
        self.game_instance_id = None
        self.game_mode_id = 2
        self.is_over = False
        self.payout_amount = 0
        self.player_id = player_id
        self.bet_amount = 0
        self.bet_placed = False
        self.deck = Deck()
        self._player_hand = []
        self._dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.player_blackjack = False
        self.dealer_blackjack = False
        self.player_bust = False
        self.dealer_bust = False
        self.winner = None

        # Deal to dealer_
        for i in range(2):
            self._player_hand.append(self.deck.deal())
            self._dealer_hand.append(self.deck.deal())

        # Check for blackjacks
        self.score_dealer_hand()
        self.score_player_hand()

        if self.player_score == 21:
            self.player_blackjack = True
        
        if self.dealer_score == 21:
            self.dealer_blackjack = True

    # Need a way to evaluate the total of hand
    def score_player_hand(self):
        hand_as_values = [card.blackjack_value for card in self._player_hand]

        # Need to keep reducing all Aces in hand should your total value be above 21
        while sum(hand_as_values) > 21 and 11 in hand_as_values:
            hand_as_values[hand_as_values.index(11)] = 1
        
        # Update the players score
        self.player_score = sum(hand_as_values)
        if self.player_score > 21:
            self.player_bust = True
            self.player_score = 0


    def score_dealer_hand(self):
        hand_as_values = [card.blackjack_value for card in self._dealer_hand]

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
        self._dealer_hand.append(self.deck.deal())
        self.score_dealer_hand()

    
    def hit(self):
        self._player_hand.append(self.deck.deal())
        self.score_player_hand()

    def dealer_plays(self):
        
        while self.dealer_score < 17 and not self.dealer_bust:
            self.takes()
            self.score_dealer_hand()

    # This is to compare the results
    def results(self):

        self.is_over = True

        # Check all blackjack conditions
        if self.player_blackjack and self.dealer_blackjack:
            self.payout_amount = self.bet_amount
            self.winner = 'dealer and house blackjack'

        elif self.player_blackjack and not self.dealer_blackjack:
            self.payout_amount = self.bet_amount * 2.5
            self.winner = 'player blackjack'
        
        elif not self.player_blackjack and self.dealer_blackjack:
            self.payout_amount = 0
            self.winner = 'house blackjack'

        # Compare scores
        else:
            if self.player_score == self.dealer_score:
                self.payout_amount = self.bet_amount
                self.winner = 'draw'

            elif self.player_score > self.dealer_score:
                self.payout_amount = self.bet_amount * 2
                self.winner = 'player wins'
            
            elif self.player_score < self.dealer_score:
                self.payout_amount = 0
                self.winner = 'house wins'


        # Set game to finished
        self.is_over = True

    def get_hands(self):
        print('PLAYERS HAND: ',self._player_hand)
        print('DEALERS HAND: ',self._dealer_hand)


    def get_player_hand(self):
        return [str(card) for card in self._player_hand]

    player_hand = property(get_player_hand)

    def get_dealer_hand(self):
        return [str(card) for card in self._dealer_hand]

    dealer_hand = property(get_dealer_hand)


test = Blackjack(1)
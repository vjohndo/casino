from model.player import Player
from model.deck import Deck

test_player = Player(1, 'John', 'john.do@email.com', 5000)


class Five_Card_Draw():

    def __init__(self, player, bet_amount = 10):
        self.player = player
        self.bet_amount = bet_amount
        self.deck = Deck()
        self.prize_dict = {
            'royal_flush': 800,
            'straight_flush': 50,
            'four_of_a_kind': 25,
            'full_house': 9,
            'flush': 6,
            'straight': 4,
            'three_of_a_kind': 3,
            'two_pair': 2,
            'jacks_or_better' : 1
        }

        for i in range(5):
            self.player.hand.append(self.deck.deal())

        # Sort hand
        self.player.hand.sort()

        print("PLAYER'S HAND:", self.player.hand)
    
    def get_hand(self):
        return self.player.get_hand()

    hand = property(get_hand)

    def get_bet(self):
        return self.bet_amount
    
    def set_bet(self, amount):
        self.bet_amount = amount
    
    bet = property(get_bet, set_bet)


    def redraw(self):
        # Input for testing
        indexes_to_redraw = input('redraw: ')
        indexes_to_redraw = [int(char) for char in indexes_to_redraw]
        print(indexes_to_redraw)
        
        for index in indexes_to_redraw:
            self.player.hand[index] = self.deck.deal()
        print(self.player.hand)

        # Sort hand
        self.player.hand.sort()
        

    def any_wins(self):
        """ Checks through all possible win combinations and returns a dictionary """
        winning_combos = {
            'royal_flush': False,
            'straight_flush': False,
            'four_of_a_kind': False,
            'full_house': False,
            'flush': False,
            'straight': False,
            'three_of_a_kind': False,
            'two_pair': False,
            'jacks_or_better' : False
        }

        # Check the players hand using the all function
        is_flush = all([card.suit == self.player.hand[0].suit for card in self.player.hand])
       
        # Check any all the rank combinations
        card_value_counts = {}
        for card in self.player.hand:
            card_value_counts[card.poker_value] = card_value_counts.get(card.poker_value, 0) + 1

        # Create a list with poker_values
        hand_as_values = [card.poker_value for card in self.player.hand]

        # Royal Flush
        if hand_as_values == [10, 11, 12, 13, 14] and is_flush:
            winning_combos['royal_flush'] = True

        # Stright Flush
        elif [(value - hand_as_values[0]) for value in hand_as_values] == [0,1,2,3,4] and is_flush:
            winning_combos['straight_flush'] = True

        # Four-of-a-kind
        elif 4 in card_value_counts.values():
            winning_combos['four_of_a_kind'] = True

        # Full House
        elif 3 in card_value_counts.values() and 2 in card_value_counts.values():
            winning_combos['full_house'] = True

        # Flush
        elif is_flush:
            winning_combos['flush'] = True

        # Straight 
        elif [(value - hand_as_values[0]) for value in hand_as_values] == [0,1,2,3,4]:
            winning_combos['straight'] = True
        
        # Three of a kind
        elif 3 in card_value_counts.values():
            winning_combos['three_of_a_kind'] = True

        # Two Pair 
        elif list(card_value_counts.values()).count(2) == 2:
            winning_combos['two_pair'] = True

        # Doubles > Jack
        for items in list(card_value_counts.items()):
            if items[1] >= 2 and items[0] >= 11:
                winning_combos['jacks_or_better'] = True

        return winning_combos


game = Five_Card_Draw(test_player,100)
game.any_wins()
# game.redraw()
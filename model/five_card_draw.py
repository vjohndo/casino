from model.player import Player
from model.deck import Deck

test_player = Player(1, 'John', 'john.do@email.com', 'haha', 5000)


class Five_Card_Draw():

    def __init__(self, player_id):
        self.game_instance_id = None
        self.is_over = False
        self.game_mode_id = 1
        self.winning_case = None
        self.payout_amount = None
        self.player_id = player_id
        self.bet_amount = 0
        self.deck = Deck()
        self.bet_placed = False
        self._hand = []
        self.prize_dict = {
            'royal_flush': 800,
            'straight_flush': 50,
            'four_of_a_kind': 25,
            'full_house': 9,
            'flush': 6,
            'straight': 4,
            'three_of_a_kind': 3,
            'two_pair': 2,
            'jacks_or_better' : 1,
            'no_win': 0
        }

        for i in range(5):
            self._hand.append(self.deck.deal())

    
    # Hand properties
    def get_hand(self):
        return [str(card) for card in self._hand]

    hand = property(get_hand)

    # Bet properties
    def get_bet(self):
        return self.bet_amount
    
    def set_bet(self, amount):
        self.bet_amount = amount
    
    bet = property(get_bet, set_bet)

    # Hand sort
    def hand_sort(self):
        self._hand.sort()

    # Hand Redraw
    def redraw(self, index_list):
        indexes_to_redraw = [int(char) for char in index_list]
        
        for index in indexes_to_redraw:
            self._hand[index] = self.deck.deal()

    # Checks for any wins
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
            'jacks_or_better' : False,
            'no_win' : False
        }

        # Check the players hand using the all function
        is_flush = all([card.suit == self._hand[0].suit for card in self._hand])
       
        # Check any all the rank combinations
        card_value_counts = {}
        for card in self._hand:
            card_value_counts[card.poker_value] = card_value_counts.get(card.poker_value, 0) + 1

        # Create a list with poker_values
        hand_as_values = [card.poker_value for card in self._hand]
        hand_as_values.sort()

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

        # Doubles > Jack or no win
        else:
            for items in list(card_value_counts.items()):
                if items[1] >= 2 and items[0] >= 11:
                    winning_combos['jacks_or_better'] = True
                else:
                    winning_combos['no_win'] = True

        return winning_combos

    # Determines payout
    def payout(self):
        win_table = self.any_wins()
        self.winning_case = [string for string in win_table.keys() if win_table[string]][0]
        self.payout_amount = self.prize_dict[self.winning_case]*self.bet_amount
        self.is_over = True

def main_test():
    game = Five_Card_Draw(test_player,100)
    game.any_wins()
    print(game.hand)
    print(game.payout()[0])
    game.redraw()
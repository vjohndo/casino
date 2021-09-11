from random import shuffle
import random

suits = {
            'S':'Spades',
            'C':'Clubs',
            'D':'Diamonds',
            'H':'Hearts'
}

suits_order = {
                'S':1,
                'C':2,
                'D':3,
                'H':4
}

ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

ranks_values_blackjack = {
            '2':2,
            '3':3,
            '4':4,
            '5':5,
            '6':6,
            '7':7,
            '8':8,
            '9':9,
            '10':10,
            'J':10,
            'Q':10,
            'K':10,
            'A':11
        }

ranks_values_poker = {
            '2':2,
            '3':3,
            '4':4,
            '5':5,
            '6':6,
            '7':7,
            '8':8,
            '9':9,
            '10':10,
            'J':11,
            'Q':12,
            'K':13,
            'A':14
        }

class Card:
    """
    A single playing Card.

    Instance Variables:
        suit
        rank
    """

    def __init__(self, rank, suit):
        self.rank = rank
        self.poker_value = ranks_values_poker[rank]
        self.blackjack_value = ranks_values_blackjack[rank]
        self.suit = suit

    def __str__(self):
        """ String representation """
        return f'{self.rank}{self.suit}'
    
    def __repr__(self):
        """ Shell representation """
        return self.__str__()

    # Both poker and blackjack don't assign value to cards suit, provides a helpful sort.
    def __eq__(self, other):
        """ Define equality """
        return ranks_values_poker[self.rank] == ranks_values_poker[other.rank]
    
    def __lt__(self, other):
        """ Define less than """
        return ranks_values_poker[self.rank] < ranks_values_poker[other.rank]
class Deck:
    """
    A deck of playing cards.

    Instance variables: none, but need a list of suits and ranks

    Implemented as a deque where if you push pop, that's the top of the stack
    """

    def __init__(self):
        self.card_stack = []
        for rank in ranks:
            for suit in suits.keys():
                self.card_stack.append(Card(rank,suit))
        
        shuffle(self.card_stack)

    def __str__(self):
        return f"[{', '.join([str(card) for card in self.card_stack])}]"
    
    def deal(self):
        return self.card_stack.pop()


# def test_code():
#     test_deck = Deck()
#     print(test_deck)
#     test_deck.deal()
#     test_deck.deal()
#     print(test_deck)

# test_code()
suits = {
            'S':'Spades',
            'C':'Clubs',
            'D':'Diamonds',
            'H':'Hearts'
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
        self.suit = suit

    def __str__(self):
        return f'{self.rank}{self.suit}'
    
    def __repr__(self):
        return self.__str__()

class Deck:
    """
    A deck of playing cards.

    Instance variables: none, but need a list of suits and ranks

    Implemented as a deque where if you push pop, that's the top of the stack
    """

    def __init__(self):
        self.card_stack = []
        for suit in suits.keys():
            for rank in ranks:
                self.card_stack.append(Card(rank,suit))
        
    def __str__(self):
        return f"[{', '.join([str(card) for card in self.card_stack])}]"

test_deck = Deck()
print(test_deck)
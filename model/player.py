class Player:
    """
    Class for a player

    Instance variables:
        > Player ID
        > Player Name
        > Player Email
        > Player Wallet
        > Players Hand 

    """
    def __init__(self, id, name, email, wallet):
        # Will be retrieved from databse
        self.id = id 
        self.name = name 
        self.email = email
        self.wallet = wallet

        # Will be supplied by the game
        self.hand = []

    def get_hand(self):
        return [str(card) for card in self.hand]

    
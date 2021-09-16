from datetime import date

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
    def __init__(self, id, name, email, passwordHash, wallet, isAdmin=False, last_login=date(1900,1,1)):
        # Will be retrieved from databse
        self.id = id 
        self.name = name 
        self.email = email
        self.passwordHash = passwordHash
        self.wallet = wallet
        self.isAdmin = isAdmin
        self.last_login = last_login

test = Player(1, 'john', 'john.do@mail', 1231, True)
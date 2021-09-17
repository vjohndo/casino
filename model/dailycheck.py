from datetime import datetime, timedelta, date

def moreThanADay(player):
    time_delta = (date.today() - player.last_login).days
    if time_delta >= 1:
        return True
    else:
        return False
class Matchup:

    home = None
    away = None
    spread = []
    over_under = []

    def __init__(self, home, away):
        self.home = home
        self.away = away

    def add_spread(self, spread):    
        self.spread.append(spread)

    def add_over_under(self, over_under):
        self.over_under.append(over_under)
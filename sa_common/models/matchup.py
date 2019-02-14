import statistics

class Matchup:

    home = None
    away = None
    spread = []
    over_under = []

    def __init__(self, home, away):
        self.home = home
        self.away = away
        self.spread = []
        self.over_under = []

    def __str__(self):
        return f"{self.away} at {self.home}, {statistics.mean(self.spread)}, {statistics.mean(self.over_under)}"

    def __repr__(self):
        return self.__str__()

    def add_spread(self, spread):    
        self.spread.append(spread)

    def add_over_under(self, over_under):
        self.over_under.append(over_under)
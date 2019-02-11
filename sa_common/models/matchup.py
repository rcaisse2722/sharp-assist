class Matchup:

    home = None
    away = None
    spread = None
    over_under = None
    predictions = []

    def __init__(self, home, away, spread, over_under):
        self.home = home
        self.away = away
        self.spread = spread
        self.over_under = over_under

    def add_predictions(self, predictions):    
        self.predictions.append(predictions)
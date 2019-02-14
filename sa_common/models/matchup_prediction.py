class MatchupPrediction:

    home = None
    away = None
    predictions = []

    def __init__(self, home, away):
        self.home = home
        self.away = away
        self.predictions = []

    def __str__(self):
        return f"{self.away} at {self.home}"

    def __repr__(self):
        return self.__str__()

    def add_predictions(self, predictions):    
        self.predictions.append(predictions)
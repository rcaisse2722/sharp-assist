class MatchupPrediction:

    home = None
    away = None
    predictions = []

    def __init__(self, home, away):
        self.home = home
        self.away = away

    def add_predictions(self, predictions):    
        self.predictions.append(predictions)
class PredictedOutcome:

    def __init__(self, home_score, away_score, over_under):
        self.home_score = home_score
        self.away_score = away_score
        self.over_under = over_under

    def to_string(self):
        return f"Away: {self.away_score} Home: {self.home_score} O/U {self.over_under}"        
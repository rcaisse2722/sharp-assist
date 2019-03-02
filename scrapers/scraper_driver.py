import sys
import os
import statistics
from oddsshark_consensus import scrape_page
from espn_scraper import scrape_lines
from cbs_scraper import scrape_scores
from sa_common.html_provider import FileHtmlProvider,UrlHtmlProvider
from sa_common.team_repository import FileTeamRepository

project_directory = os.path.dirname(os.path.realpath('__file__'))

# Initialize Team Provider
team_repository = FileTeamRepository(os.path.join(project_directory, "sa_common", "team_maps", "ncaab.csv"))

# Used for debugging/development, read the data from sample_data directory
sample_prediction_file = "oddsshark_consensus_ncaab_2019_02_12.html"
sample_lines_file = "espn_ncaab_2019_02_12.html"
predictions_provider = FileHtmlProvider(os.path.join(project_directory, "scrapers", "sample_data", sample_prediction_file))
lines_provider = FileHtmlProvider(os.path.join(project_directory, "scrapers", "sample_data", sample_lines_file))

# Real Data (TODO make URL configurable)
#predictions_provider = UrlHtmlProvider("https://www.oddsshark.com/ncaab/computer-picks")
#lines_provider = UrlHtmlProvider("http://www.espn.com/mens-college-basketball/lines")

print("****** RETRIEVING MATCHUPS *********")
matchups = scrape_lines(lines_provider, team_repository, True)

print("****** RETRIEVING PREDICTIONS *********")
predictions = scrape_page(predictions_provider, team_repository, True)

print(f"Retrieved {len(matchups)} matchups and {len(predictions)} predictions")

matchups.sort(key=lambda x: x.away.teamid)
predictions.sort(key=lambda x: x.away.teamid)

sharp_outcome_spread = [] # will contain a list of tuples (score diff, team pick, matchup object)
sharp_outcome_ou = [] # will contain a list of tuples (score diff, team pick, matchup object)

# Scraping complete, let's apply the logic
for matchup in matchups:
    prediction = next((x for x in predictions if x.away.teamid == matchup.away.teamid), None)
    if prediction is None:
        print(f"Failed to find matching prediction for matchup: {matchup}")
    else:
        if(len(matchup.spread) > 0):
            mean_spread = statistics.mean(matchup.spread)
            predicted_spread = -(prediction.predictions[0].away_score - prediction.predictions[0].home_score)
            spread_differential = mean_spread - predicted_spread

            pick = None # None represents push, prediction is exactly in line with actual spread
            if(spread_differential > 0):
                pick = matchup.away
            elif(spread_differential < 0):
                pick = matchup.home        

            sharp_outcome_spread.append((abs(spread_differential), pick, matchup))

        if(len(matchup.over_under) > 0):
            mean_over_under = statistics.mean(matchup.over_under)
            over_under_differential = (prediction.predictions[0].away_score + prediction.predictions[0].home_score) - mean_over_under
            
            isOver = True
            if(over_under_differential < 0): # ignoring push if predicted score is exact
                isOver = False

            sharp_outcome_ou.append((abs(over_under_differential), isOver, matchup))

sharp_outcome_spread.sort(key=lambda x: x[0], reverse=True)

print("SPREAD PICKS")
[print(f"{x[0]:.2f} PICK {x[1]} MATCHUP {x[2]}") for x in sharp_outcome_spread]

sharp_outcome_ou.sort(key=lambda x: x[0], reverse=True)

print("O/U PICKS")
[print(f"{x[0]:.2f} OVER? {x[1]} MATCHUP {x[2]}") for x in sharp_outcome_ou]


# # Get results of previous days game
sample_scores_file = "cbs_ncaab_2019_02_13.html"
scores_provider = FileHtmlProvider(os.path.join(project_directory, "scrapers", "sample_data", sample_scores_file))

scrape_scores(scores_provider, team_repository, True)
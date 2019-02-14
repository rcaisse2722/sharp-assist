import sys
import os
import statistics
from oddsshark_consensus import scrape_page
from espn_scraper import scrape_lines
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

print("****** RETRIEVING MATCHUPS *********")
matchups = scrape_lines(lines_provider, team_repository, True)

print("****** RETRIEVING PREDICTIONS *********")
predictions = scrape_page(predictions_provider, team_repository, True)

print(f"Retrieved {len(matchups)} matchups and {len(predictions)} predictions")

matchups.sort(key=lambda x: x.away.teamid)
predictions.sort(key=lambda x: x.away.teamid)

sharp_outcome = [] # will contain a list of tuples (score diff, matchup object)

# Scraping complete, let's apply the logic
for matchup in matchups:
    prediction = next((x for x in predictions if x.away.teamid == matchup.away.teamid), None)
    if prediction is None:
        print(f"Failed to find matching prediction for matchup: {matchup}")
    else:
        mean_spread = statistics.mean(matchup.spread)
        predicted_spread = -(prediction.predictions[0].away_score - prediction.predictions[0].home_score)
        spread_differential = mean_spread - predicted_spread

        pick = None # None represents push, prediction is exactly in line with actual spread
        if(spread_differential > 0):
            pick = matchup.away
        elif(spread_differential < 0):
            pick = matchup.home        

        sharp_outcome.append((abs(spread_differential), pick, matchup))

sharp_outcome.sort(key=lambda x: x[0], reverse=True)

[print(f"{x[0]} PICK {x[1]} MATCHUP {x[2]}") for x in sharp_outcome]
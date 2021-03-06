import sys
import os
import statistics
import yaml
from scrapers.oddsshark_consensus import scrape_page
from scrapers.espn_scraper import scrape_lines
from scrapers.cbs_scraper import scrape_scores
from sa_common.html_provider import FileHtmlProvider,UrlHtmlProvider
from sa_common.team_repository import FileTeamRepository

project_directory = os.path.dirname(os.path.realpath('__file__'))

# Parse config file
config = yaml.load(open(os.path.join(project_directory, "config.yaml"), 'r'), Loader=yaml.Loader)

# Initialize Team Provider
team_repository = FileTeamRepository(os.path.join(project_directory, os.path.join(*config["team_repo"])))

if config["debug"] == True:
    predictions_provider = FileHtmlProvider(os.path.join(project_directory, os.path.join(*config["debug_data"]["predictions"])))
    lines_provider = FileHtmlProvider(os.path.join(project_directory, os.path.join(*config["debug_data"]["lines"])))
else:
    predictions_provider = UrlHtmlProvider(config["live_data"]["predictions"])
    lines_provider = UrlHtmlProvider(config["live_data"]["lines"])

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
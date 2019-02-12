import sys
import os
from oddsshark_consensus import scrape_page
from espn_scraper import scrape_lines
from sa_common.html_provider import FileHtmlProvider,UrlHtmlProvider
from sa_common.team_repository import FileTeamRepository

project_directory = os.path.dirname(os.path.realpath('__file__'))

# Initialize Team Provider
team_repository = FileTeamRepository(os.path.join(project_directory, "sa_common", "team_maps", "ncaab.csv"))

# Used for debugging/development, read the data from sample_data directory
sample_prediction_file = "oddsshark_consensus_ncaab_2019_02_11.html"
sample_lines_file = "espn_ncaab_2019_02_11.html"
predictions_provider = FileHtmlProvider(os.path.join(project_directory, "scrapers", "sample_data", sample_prediction_file))
lines_provider = FileHtmlProvider(os.path.join(project_directory, "scrapers", "sample_data", sample_lines_file))

print("****** RETRIEVING MATCHUPS *********")
matchups = scrape_lines(lines_provider, team_repository, True)

print("****** RETRIEVING PREDICTIONS *********")
predictions = scrape_page(predictions_provider, team_repository, True)

print(f"Retrieved {len(matchups)} matchups and {len(predictions)} predictions")
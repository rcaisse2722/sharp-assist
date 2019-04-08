import sys
import os
import statistics
import yaml
from scrapers.oddsshark_consensus import scrape_page
from scrapers.cbs_scraper import scrape_scores
from sa_common.html_provider import FileHtmlProvider,UrlHtmlProvider
from sa_common.team_repository import FileTeamRepository

project_directory = os.path.dirname(os.path.realpath('__file__'))

# Parse config file
config = yaml.load(open(os.path.join(project_directory, "config.yaml"), 'r'), Loader=yaml.Loader)

# Initialize Team Provider
team_repository = FileTeamRepository(os.path.join(project_directory, os.path.join(*config["team_repo"])))

if config["debug"] == True:
    scores_provider = FileHtmlProvider(os.path.join(project_directory, os.path.join(*config["debug_data"]["scores"])))
else:
    scores_provider = UrlHtmlProvider(config["live_data"]["scores"])

scrape_scores(scores_provider, team_repository, True)


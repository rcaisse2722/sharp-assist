import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from sa_common.models.baseteam import BaseTeam
from sa_common.models.matchup import Matchup
from bs4 import BeautifulSoup
from tidylib import tidy_document

def scrape_scores(data_provider, team_repository, isVerbose = False):
    global verbose
    verbose = isVerbose

    document, errors = tidy_document(data_provider.get_html())

    parsed_data = BeautifulSoup(document, 'html.parser')

    games = parsed_data.find_all("div", {"class" : "in-progress-table"}) 
    
    for game in games:
        away_team = " ".join(game.find("a", {"class" : "team"}).text.strip().split())
        print(away_team)
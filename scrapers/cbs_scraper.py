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
        teams = game.find_all("a", {"class" : "team"})
        
        try:
            away_team_str = " ".join(teams[0].text.strip().split())
            home_team_str = " ".join(teams[1].text.strip().split())
        except:
            print("Error parsing score from CBS")
            continue

        home_team = team_repository.get_team(home_team_str)
        if(home_team == None):
            print(f"Team {home_team_str} not found in repository")
            break
        away_team = team_repository.get_team(away_team_str)
        if(away_team == None):
            print(f"Team {away_team_str} not found in repository")
            break
        away_team_score = extract_score(teams[0].parent)
        home_team_score = extract_score(teams[1].parent)

        print(f"{away_team_str} at {home_team_str}: {away_team_score} - {home_team_score}")
        

def extract_score(parent_tag):
    lastTag = None
    for child in parent_tag.next_siblings:
        if child == '\n':
            continue
        elif child.name == 'td':
            lastTag = child
    return int(lastTag.text)
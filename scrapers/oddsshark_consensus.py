import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from sa_common.models.baseteam import BaseTeam
from sa_common.models.matchup_prediction import MatchupPrediction
from sa_common.models.predicted_outcome import PredictedOutcome

from bs4 import BeautifulSoup

def scrape_page(data_provider, team_repository, is_verbose = False):

    global verbose
    verbose = is_verbose

    parsed_data = BeautifulSoup(data_provider.get_html(), 'html.parser')

    parent_tag = parsed_data.find("div", {"id": "block-system-main"})

    if parent_tag == None:
        print("Failed to parse main block from OddsShark")
        return

    all_games = parent_tag.find_all("table", {"class": "base-table"})

    if len(all_games) == 0:
        print("Failed to parse games from OddsShark")
        return

    predictions = []

    for game_tag in all_games:
        teams_tag_wrapper = game_tag.find("div", {"class" : "caption-wrapper"})
        if teams_tag_wrapper is None:
            print("Failed to find team wrapper, but continuing")
            continue

        teams_tag = teams_tag_wrapper.find_all("span", {"class" : "name-short"})
        if teams_tag is None or len(teams_tag) != 2:
            print("Failed to parse teams tag")
            break

        home_team_str = teams_tag[1].string.strip(';')
        home_team = team_repository.get_team(home_team_str)
        if(home_team == None):
            print(f"Team {home_team_str} not found in repository")
            break
        away_team_str = teams_tag[0].string.strip(';')
        away_team = team_repository.get_team(away_team_str)
        if(away_team == None):
            print(f"Team {away_team_str} not found in repository")
            break

        matchup = MatchupPrediction(home_team, away_team)        

        if(verbose):
            print(away_team.teamname + " at " + home_team.teamname)

        game_data = game_tag.find("tbody").find_all("tr")
        matchup.add_predictions(parse_predicted_score(game_data[0]))

        predictions.append(matchup)

    return predictions

# < tr >
# < td > < img
# src = "/sites/all/themes/skeletontheme/images/os_logo_20x20.png"
# height = "12px"
# width = "12px"
# align = "bottom" / > Predicted
# Score < / td >
# < td > 12.8 - 30.4 < / td >
# < td > 43.2 < / td >
# < / tr >
def parse_predicted_score(row_tag):
    score_tag = row_tag.find_all("td")
    if(len(score_tag) != 3):
        print("Failed to parse score tag: {0}".format(row_tag))
        return None
    split_string = score_tag[1].string.split('-')
    if(len(split_string) != 2):
        print("Failed to parse score tag {0}".format(row_tag))
        return None

    prediction = PredictedOutcome(float(split_string[1].strip()), float(split_string[0].strip()), score_tag[2].string)
    if(verbose):
        print(f"{prediction.to_string()}")

    return prediction
import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from sa_common.models.baseteam import BaseTeam
from sa_common.models.matchup import Matchup
from bs4 import BeautifulSoup
from tidylib import tidy_document

# TODO Move these into constants file in sa_common? May be useful in other scrapers
TIME_REGEX = r'^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
RANKING_REGEX = r'\#[0-9]{1,2}'

def scrape_lines(data_provider, team_repository, isVerbose = False):
    global verbose
    verbose = isVerbose

    document, errors = tidy_document(data_provider.get_html())

    parsed_data = BeautifulSoup(document, 'html.parser')

    parent_tag = parsed_data.find("div", {"class": "mod-container mod-table mod-no-header"}).find("div", {"class": "mod-content"})
    
    if parent_tag == None:
        print("Failed to parse main block from ESPN lines")
        return    

    table_data = parent_tag.find("table", {"class" : "tablehead"})
    matchups = []
    current_matchup = None

    for child in table_data.find_all("tr"):
        if "class" in child.attrs:
            # Start of new game
            if child.attrs["class"][0] == "stathead":
                away_team_str, home_team_str = scrape_teams(child)
                home_team = team_repository.get_team(home_team_str)
                if(home_team == None):
                    print(f"Team {home_team_str} not found in repository")
                    break
                away_team = team_repository.get_team(away_team_str)
                if(away_team == None):
                    print(f"Team {away_team_str} not found in repository")
                    break

                if(verbose):
                    print("Starting new game")
                    print(f"{away_team.teamname} at {home_team.teamname}")
                
                if(current_matchup != None):
                    matchups.append(current_matchup)

                current_matchup = Matchup(home_team, away_team)

            # Line data from for one book
            elif child.attrs["class"][0] == "oddrow" or child.attrs["class"][0] == "evenrow":
                book_name, spread, over_under = scrape_book_data(child)
                if(spread is None and over_under is None):
                    print(f"No data found for {book_name}")
                    continue

                if(verbose):
                    print(f"{book_name}: Spread: {spread} O/U: {over_under}")

                if(spread != None):
                    current_matchup.add_spread(spread)
                if(over_under != None):
                    current_matchup.add_over_under(over_under)
    
    if(current_matchup != None):
        matchups.append(current_matchup)

    return matchups

                 


# Scrape team names
def scrape_teams(matchup_tag):
    split_string = [x.strip(',') for x in matchup_tag.td.text.split()]
    # List of strings is of the form (for example):
    # [0] North
    # [1] Carolina
    # [2] at
    # [3] Duke
    # [4] 5:30
    # [5] PM
    # So find the index of 'at' and the index of the game time to extract teams
    at_index = split_string.index('at')
    gametime_index = [i for i, item in enumerate(split_string) if re.search(TIME_REGEX, item)][0]

    away_team_name = " ".join(split_string[0:at_index])
    home_team_name = " ".join(split_string[at_index + 1:gametime_index])
    #away_team_name = " ".join([e for i, e in enumerate(split_string) if i in [0, at_index - 1]])
    #home_team_name = " ".join([e for i, e in enumerate(split_string) if i in [at_index + 1, gametime_index - 1]])

    # remove potential ranking from strings ('#3 Kansas')
    return [re.sub(RANKING_REGEX, '', x).strip() for x in [away_team_name, home_team_name]]

# Scrape line and over/under data for an individual book
# <tr class="oddrow">
#     <td>Westgate</td>
#     <td style="text-align:center;">
#         <table cellspacing="1" cellpadding="3" class="tablehead">
#             <tr>
#                 <td width="50%">-5.5<br />+5.5</td>
#                 <td width="50%">PENN: -110<br />COR: -110</td>
#             </tr>
#         </table>
#     </td>
#     <td style="text-align:center;">
#         <table cellspacing="1" cellpadding="3" class="tablehead">
#             <tr>
#                 <td width="50%">139</td>
#                 <td width="50%">o: -110<br />u: -110</td>
#             </tr>
#         </table>
#     </td>
#     <td style="text-align:center;">N/A</td>
#     </td>
# </tr>
def scrape_book_data(book_tag):
    first_row = book_tag.td
    book_name = first_row.text.strip().replace('\r','').replace('\n','').replace('  ', '')
    spread = None
    over_under = None
    retrieved_spread = False
    for child in first_row.next_siblings:
        if child == '\n':
            continue
        elif retrieved_spread == False:
            try:
                if("EVEN" in child.text):
                    spread = 0
                else:
                    spread = float(child.find("td").text.split()[0])
            except:
                spread = None
            retrieved_spread = True
        else:
            try:
                over_under = float(child.find("td").text.strip())
            except:
                over_under = None
            break

    return book_name,spread,over_under
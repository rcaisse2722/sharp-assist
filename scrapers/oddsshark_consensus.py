import sys
from bs4 import BeautifulSoup

def scrape_page(path):
    # Read from file (TEST ONLY, comment out)
    with open(path, 'r') as testFile:
        doc = testFile.read()

    parsed_data = BeautifulSoup(doc, 'html.parser')

    # Read from NY Post
    #doc = urllib2.urlopen(path)
    # Grab the lines div
    parent_tag = parsed_data.find("div", {"id": "block-system-main"})

    if parent_tag == None:
        print("Failed to parse main block from OddsShark")
        return

    all_games = parent_tag.find_all("table", {"class": "base-table"})

    if len(all_games) == 0:
        print("Failed to parse games from OddsShark")
        return

    success = True
    for game_tag in all_games:
        teams_tag_wrapper = game_tag.find("div", {"class" : "caption-wrapper"})
        if teams_tag_wrapper is None:
            print("Failed to find team wrapper, but continuing")
            continue

        teams_tag = teams_tag_wrapper.find_all("span", {"class" : "name-short"})
        if teams_tag is None or len(teams_tag) != 2:
            print("Failed to parse teams tag")
            success = False
            break

        home_team = teams_tag[0].string
        away_team = teams_tag[1].string

        print(home_team + " at " + away_team)

        game_data = game_tag.find("tbody").find_all("tr")
        parse_predicted_score(game_data[0])

    return success

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
        raise
    split_string = score_tag[1].string.split('-')
    if(len(split_string) != 2):
        print("Failed to parse score tag {0}".format(row_tag))
        raise
    away_score = float(split_string[0].strip())
    home_score = float(split_string[1].strip())
    over_under = score_tag[2].string

    print("Away: {0} Home: {1} O/U {2}".format(away_score, home_score, over_under))
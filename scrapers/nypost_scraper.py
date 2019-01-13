import sys
import urllib2
from bs4 import BeautifulSoup

'''
Parse HTML of NY Post 
'''
def scrape_page(path, sport):

    # Read from file (TEST ONLY, comment out)
    # with open(path, 'r') as testFile:
    #    doc = testFile.read();

    # Read from NY Post
    doc = urllib2.urlopen(path)

    parsed_data = BeautifulSoup(doc, 'html.parser')

    # Grab the lines div
    parent_tag = parsed_data.find_all("div", { "class": "box no-mobile module widget_nypost_post_line_widget"})

    if len(parent_tag) == 0:
        print "Failed to parse line data from NY post."
        return

    # Grab section
    sport_tag = parent_tag[0].find("div", {"class" : str.format("sport-scores {0}", sport)})
    games = sport_tag.find("tbody").find_all("tr")
    print str.format("Found {0} games", len(games))

    for game in games:
        favorite = game.find("td", {"class" : "sport-score-team favorite"}).string
        underdog = game.find("td", {"class": "sport-score-team underdog"}).string
        line = game.find("td", {"class": "current-line"}).string
        # FIXME regular str.format doesn't take unicode
        # print str.format("{0} vs. {1}: {2}", favorite, underdog, line)
        print favorite + " vs. " + underdog + ": " + line



import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from sa_common.models.baseteam import BaseTeam
from bs4 import BeautifulSoup
from tidylib import tidy_document

# TODO Move these into constants file in sa_common? May be useful in other scrapers
TIME_REGEX = '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$'
RANKING_REGEX = r'\#[0-9]{1,2}'

def scrape_lines(path, isVerbose = False):
    global verbose
    verbose = isVerbose

    # Read from file (TEST ONLY, comment out)
    with open(path, 'r', errors="surrogateescape") as testFile:
        doc = testFile.read()
    #doc = urllib2.urlopen(path)

    # TODO Log errors?
    document, errors = tidy_document(doc)

    parsed_data = BeautifulSoup(document, 'html.parser')

    parent_tag = parsed_data.find("div", {"class": "mod-container mod-table mod-no-header"}).find("div", {"class": "mod-content"})
    
    if parent_tag == None:
        print("Failed to parse main block from ESPN lines")
        return    

    table_data = parent_tag.find("table", {"class" : "tablehead"})
    
    for child in table_data.find_all("tr"):
        if "class" in child.attrs:
            # Start of new game
            if child.attrs["class"][0] == "stathead":
                awayTeamString, homeTeamString = scrape_teams(child)
                if(verbose):
                    print("Starting new game")
                    print(f"{awayTeamString} at {homeTeamString}")

            # Line data from for one book
            elif child.attrs["class"][0] == "oddrow" or child.attrs["class"][0] == "evenrow":
                bookName, spread, overUnder = scrape_book_data(child)
                if(spread is None or overUnder is None):
                    print(f"No data for {bookName}")
                elif(verbose):
                    print(f"{bookName}: Spread: {spread} O/U: {overUnder}")


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
    atIndex = split_string.index('at')
    gametimeIndex = [i for i, item in enumerate(split_string) if re.search(TIME_REGEX, item)][0]
    awayTeamName = " ".join([e for i, e in enumerate(split_string) if i in [0, atIndex - 1]])
    homeTeamName = " ".join([e for i, e in enumerate(split_string) if i in [atIndex + 1, gametimeIndex - 1]])

    # remove potential ranking from strings ('#3 Kansas')
    return [re.sub(RANKING_REGEX, '', x).strip() for x in [awayTeamName, homeTeamName]]

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
    firstRow = book_tag.td
    bookName = firstRow.text.strip().replace('\r','').replace('\n','').replace('  ', '')
    spread = None
    overUnder = None
    retrievedSpread = False
    for child in firstRow.next_siblings:
        if child == '\n':
            continue
        elif retrievedSpread == False:
            try:
                spread = float(child.find("td").text.split()[0])
            except:
                spread = None
            retrievedSpread = True
        else:
            try:
                overUnder = float(child.find("td").text.strip())
            except:
                overUnder = None
            break

    return bookName,spread,overUnder

    #data = book_tag.find_all("td")
    #if len(data) != 4:
    #    print("Error scraping book data")
    #    return
    
    #book_name = data[0].value
    #print(book_name)

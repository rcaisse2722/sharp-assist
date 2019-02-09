import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from sa_common.models.baseteam import BaseTeam
from bs4 import BeautifulSoup
from tidylib import tidy_document

def scrape_lines(path, isVerbose = False):
    global verbose
    verbose = isVerbose

    # Read from file (TEST ONLY, comment out)
    with open(path, 'r', errors="surrogateescape") as testFile:
        doc = testFile.read()
    #doc = urllib2.urlopen(path)

    options = {
        str("quiet"): True,
        str("show-errors"): 0,
        str("force-output"): True,
        str("numeric-entities"): True,
        str("show-warnings"): False,
        str("indent"): False,
        str("tidy-mark"): False,
        str("wrap"): 0
        };

    document, errors = tidy_document(doc, options=options)

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
                print("Starting new game")
            # Line data from for one book
            elif child.attrs["class"][0] == "oddrow" or child.attrs["class"][0] == "evenrow":
                print("Book data")
                scrape_book_data(child)


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
    print(firstRow)
    for child in firstRow.next_siblings:
        if child is Tag:
            print(child)
        else:
            print("Nope")

    #data = book_tag.find_all("td")
    #if len(data) != 4:
    #    print("Error scraping book data")
    #    return
    
    #book_name = data[0].value
    #print(book_name)

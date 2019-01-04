import sys
from bs4 import BeautifulSoup

def scrape_page(path):
    # Read from file (TEST ONLY, comment out)
    with open(path, 'r') as testFile:
        doc = testFile.read();

    # Read from NY Post
    #doc = urllib2.urlopen(path)
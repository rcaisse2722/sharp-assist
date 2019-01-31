import sys
import os
from oddsshark_consensus import scrape_page

projectDirectory = os.path.dirname(os.path.realpath('__file__'))
sampleDataFile = "oddsshark_consensus_nfl.html"

matchups = scrape_page(f"{projectDirectory}\\scrapers\\sample_data\\{sampleDataFile}")
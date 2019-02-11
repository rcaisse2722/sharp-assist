import sys
import os
from oddsshark_consensus import scrape_page
from espn_scraper import scrape_lines

projectDirectory = os.path.dirname(os.path.realpath('__file__'))
samplePredictionFile = "oddsshark_consensus_nfl.html"
sampleLinesFile = "espn_ncaab.html"

lines = scrape_lines(os.path.join(projectDirectory, "scrapers", "sample_data", sampleLinesFile), True)
matchups = scrape_page(os.path.join(projectDirectory, "scrapers", "sample_data", samplePredictionFile), True)
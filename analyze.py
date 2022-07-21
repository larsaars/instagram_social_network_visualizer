#!/usr/bin/env python3
"""
scrape instagram social bubbles
"who follows whom"

begin with scraping with selenium
afterwards scrape for depth 3+ with the api with a random ig account
"""

import os
from dotenv import load_dotenv
from scrape_ig_api import query_ig_api
from relational_clustering import find_nodes_and_edges
import json
from scrape_ig_selenium import scrape_with_selenium

# load .env file
load_dotenv()

# load env variables
IG_SELENIUM_USERNAME = os.getenv('IG_SELENIUM_USERNAME')
IG_SELENIUM_PASSWORD = os.getenv('IG_SELENIUM_PASSWORD')

IG_API_PASSWORD = os.getenv('IG_API_PASSWORD')
IG_API_USERNAME = os.getenv('IG_API_USERNAME')

MAX_FOLLOWERS_API = os.getenv('MAX_FOLLOWERS_API')
MAX_FOLLOWERS_SELENIUM = os.getenv('MAX_FOLLOWERS_SELENIUM')

# 1 - my followers
# 2 - followers of my followers
# 3 - followers of followers of my followers etc.
ANALYZE_DEPTH = int(os.getenv('ANALYZE_DEPTH'))
MIN_NUM_OF_RELATIONS = int(os.getenv('MIN_NUM_OF_RELATIONS'))

PATH_TO_EDGES_FILE = os.getenv('PATH_TO_EDGES_FILE')
PATH_TO_NODES_FILE = os.getenv('PATH_TO_NODES_FILE')


def main():
    # in between always save the results ('followers.json')

    # dict of user usernames and their followings
    # in the format:
    # {
    #     'username': ['follower1', 'follower2', ...],
    #     'username2': ['follower1', 'follower2', ...],
    #     ...
    # }

    # scrape with selenium
    usernames_to_scrape = scrape_with_selenium(IG_SELENIUM_USERNAME, IG_SELENIUM_PASSWORD, MAX_FOLLOWERS_SELENIUM,
                                               ANALYZE_DEPTH)

    # continue to scrape with api for depth 3+
    query_ig_api(usernames_to_scrape, IG_API_USERNAME, IG_API_PASSWORD, MAX_FOLLOWERS_API, ANALYZE_DEPTH)

    # analyze relations via relational clustering
    with open('followers.json', 'r') as f:
        all_followers = json.load(f)

    find_nodes_and_edges(all_followers, MIN_NUM_OF_RELATIONS, PATH_TO_EDGES_FILE, PATH_TO_NODES_FILE)


if __name__ == '__main__':
    main()

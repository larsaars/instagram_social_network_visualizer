"""
analyze instagram follower social bubbles
"who follows whom"
"""

import os
from dotenv import load_dotenv
from instagrapi import Client

# load .env file
load_dotenv()

# load env variables
IG_USERNAME = os.getenv('IG_USERNAME')
IG_PASSWORD = os.getenv('IG_PASSWORD')
ANALYZE_DEPTH = int(os.getenv('ANALYZE_DEPTH'))
MAX_FOLLOWERS = int(os.getenv('MAX_FOLLOWERS'))

# authenticate
client = Client()
client.login(IG_USERNAME, IG_PASSWORD)

user_followings = []


# find all followers till wished depth of analysis recursively
def query_followings(user_id, depth):
    if depth == 0:
        return

    # fetch following users
    following = client.user_following(user_id=user_id, amount=MAX_FOLLOWERS, use_cache=True)

    # recursively call query_followers for each following
    for id in following:
        pass

        # query this users followings
        # query_followings(id, depth - 1)


query_followings(client.user_id, ANALYZE_DEPTH)

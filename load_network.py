"""
analyze instagram following social bubbles
"who follows whom"
"""

import os
from dotenv import load_dotenv
from instagrapi import Client
import json

# dict of user usernames and their followings
# in the format:
# {
#     'username': ['following1', 'following2', ...],
#     'username2': ['following1', 'following2', ...],
#     ...
# }
all_followings = dict()


def main():
    print('Query followings...')

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

    # find all followers till wished depth of analysis recursively
    def query_followings(current_user_id, current_username, depth):
        if depth == 0:
            return

        if current_username not in all_followings:
            # inform over the progress
            print(current_username)

            # fetch following users
            following = client.user_following(user_id=current_user_id, amount=MAX_FOLLOWERS, use_cache=True)

            # add to dict of following users
            all_followings[current_username] = list()

            # recursively call query_followers for each following
            for user_id in following:
                username = following[user_id].username
                # add username to following list
                all_followings[current_username].append(username)

                # query this user's followings
                query_followings(user_id, username, depth - 1)

    # start query_followings from base user
    query_followings(client.user_id, client.username, ANALYZE_DEPTH)

    print('Finished queries, saving to file')


def save_to_file():
    with open('followings.json', 'w') as f:
        json.dump(all_followings, f)


if __name__ == '__main__':
    try:
        main()
        save_to_file()
    except KeyboardInterrupt as e:
        # save interrupted progress as well
        save_to_file()
        exit(0)

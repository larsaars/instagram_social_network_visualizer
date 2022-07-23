from instagrapi import Client
import json


def query_ig_api(usernames_to_be_scraped: set, ig_username, ig_password, max_followers, analyze_depth):
    # depths 1 and 2 have already been scraped over selenium
    analyze_depth -= 2

    if analyze_depth <= 0:
        print('Reached max depth, stopping scraping')
        return

    print('Query followers via API (depth 3+)...')

    with open('followers.json', 'r') as f:
        all_followers = json.load(f)

    all_followers['version'] = 2

    # authenticate
    client = Client()
    client.login(ig_username, ig_password)

    # find all followers till wished depth of analysis recursively
    def query_followings(current_user_id, current_username, depth):
        if depth <= 0:
            return

        if current_username not in all_followers:
            # inform over the progress
            print(current_username)

            # fetch following users
            followers = client.user_followers(user_id=current_user_id, amount=max_followers, use_cache=True)

            # add to dict of following users
            all_followers[current_username] = list()

            # recursively call query_followers for each following
            for user_id in followers:
                this_username = followers[user_id].username
                # add username to following list
                all_followers[current_username].append(username)

                # query this user's followings
                query_followings(user_id, this_username, depth - 1)

    # start query_followings from base user
    try:
        for username in usernames_to_be_scraped:
            query_followings(username, username, analyze_depth)
    except Exception as e:
        print(e)

    # save to file
    with open('followers.json', 'w') as f:
        json.dump(all_followers, f)

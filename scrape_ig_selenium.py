import json
import os
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from random import uniform

TIMEOUT = 15


def scrape_with_selenium(ig_username, ig_password, load_max_followers, analyze_depth) -> set:
    # dict with all followers
    all_followers = dict()

    # authenticate
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--log-level=3")
    # mobile_emulation = {
    #     "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, "
    #                  "like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"
    # }

    # options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = uc.Chrome(options=options)
    bot.set_window_size(600, 1000)

    bot.get('https://www.instagram.com/accounts/login/')

    time.sleep(2)

    # allow cookies
    bot.find_element(By.XPATH, '/html/body/div[4]/div/div/button[1]').click()

    time.sleep(uniform(2, 2.5))

    print("Logging in...")

    user_element = WebDriverWait(bot, TIMEOUT).until(
        presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))

    user_element.send_keys(ig_username)

    pass_element = WebDriverWait(bot, TIMEOUT).until(
        presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))

    pass_element.send_keys(ig_password)

    login_button = WebDriverWait(bot, TIMEOUT).until(
        presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))

    time.sleep(0.4)

    login_button.click()

    print("Logged in!")

    time.sleep(uniform(6, 9))

    def scrape_followers(username) -> set:
        # go to profile page of user
        bot.get(f'https://www.instagram.com/{username}/followers/')

        time.sleep(uniform(8, 10))

        users = set()

        # scroll down the follower list completely to load all followers
        dialog_body = bot.find_element(By.XPATH,
                                       '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div['
                                       '2]/div/div/div/div/div/div/div/div[2]')

        scroll, last_scroll_top = 0, -1

        while scroll < load_max_followers:
            bot.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight * 4;',
                dialog_body)

            time.sleep(uniform(1, 2))
            scroll += 1

            # break if scroll is at the bottom (scroll top does not change after scrolling)
            new_scroll_top = int(dialog_body.get_attribute('scrollTop'))
            if last_scroll_top == new_scroll_top:
                break

            last_scroll_top = new_scroll_top

        # get all followers (list items)
        follower_list_items = bot.find_elements(By.XPATH,
                                                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div['
                                                '2]/div/div/div/div/div/div/div/div[2]//li')

        for li in follower_list_items:
            users.add(li.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')[3])

        # add to dict of followers
        all_followers[username] = list(users)

        # return followers
        return users

    # start scraping according to depth
    followers_for_depth_3plus = set()
    if analyze_depth >= 1:
        followers_for_depth_3plus = scrape_followers(ig_username)

        if analyze_depth >= 2:
            for follower in followers_for_depth_3plus:
                followers_for_depth_3plus.update(scrape_followers(follower))

    # save json file
    with open('followers.json', 'w') as f:
        json.dump(all_followers, f)

    # exit selenium
    bot.quit()

    return followers_for_depth_3plus


if __name__ == '__main__':
    # load environment variables
    from dotenv import load_dotenv

    load_dotenv()

    IG_SELENIUM_USERNAME = os.getenv('IG_SELENIUM_USERNAME')
    IG_SELENIUM_PASSWORD = os.getenv('IG_SELENIUM_PASSWORD')
    MAX_SCROLLING_SELENIUM = int(os.getenv('MAX_SCROLLING_SELENIUM'))

    # scrape
    print(scrape_with_selenium(IG_SELENIUM_USERNAME, IG_SELENIUM_PASSWORD, MAX_SCROLLING_SELENIUM, 2))

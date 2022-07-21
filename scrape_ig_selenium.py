import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from random import uniform

TIMEOUT = 15


def scrape_with_selenium(ig_username, ig_password, load_max_followers, analyze_depth) -> set:
    # dict with all followers
    all_followers = dict()

    # authenticate
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, "
                     "like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"
    }

    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    bot.set_window_size(600, 1000)

    bot.get('https://www.instagram.com/accounts/login/')

    time.sleep(2)

    print("Logging in...")

    user_element = WebDriverWait(bot, TIMEOUT).until(
        presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')))

    user_element.send_keys(ig_username)

    pass_element = WebDriverWait(bot, TIMEOUT).until(
        presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')))

    pass_element.send_keys(ig_password)

    login_button = WebDriverWait(bot, TIMEOUT).until(
        presence_of_element_located((
            By.XPATH, '//*[@id="loginForm"]/div[1]/div[6]/button')))

    time.sleep(0.4)

    login_button.click()

    print("Logged in!")

    time.sleep(5)

    def scrape_followers(username) -> set:
        # go to profile page of user
        bot.get(f'https://www.instagram.com/{username}/followers/')

        time.sleep(uniform(2, 4))

        users = set()

        for _ in range(round(load_max_followers // 10)):

            ActionChains(bot).send_keys(Keys.END).perform()

            time.sleep(uniform(1, 2))

            followers = bot.find_elements(
                By.XPATH,
                '//*[@id="react-root"]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')

            # Getting url from href attribute
            for i in followers:
                if i.get_attribute('href'):
                    users.add(i.get_attribute('href').split("/")[3])
                else:
                    continue

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

    # exit selenium
    bot.quit()

    return followers_for_depth_3plus


if __name__ == '__main__':
    # load environment variables
    from dotenv import load_dotenv

    load_dotenv()

    IG_SELENIUM_USERNAME = os.getenv('IG_SELENIUM_USERNAME')
    IG_SELENIUM_PASSWORD = os.getenv('IG_SELENIUM_PASSWORD')
    MAX_FOLLOWERS_SELENIUM = os.getenv('MAX_FOLLOWERS_SELENIUM')
    ANALYZE_DEPTH = int(os.getenv('ANALYZE_DEPTH'))

    # scrape
    print(scrape_with_selenium(IG_SELENIUM_USERNAME, IG_SELENIUM_PASSWORD, MAX_FOLLOWERS_SELENIUM, ANALYZE_DEPTH))

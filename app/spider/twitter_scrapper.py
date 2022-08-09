from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from .common import wait_till_present, scrolling_loop
from .data_model import Post
from .scrapper_config import twitter_xpath_headless

import sys
import logging
from logging import StreamHandler, Formatter

import urllib.request
import uuid

USER = "oksigeno1"
MY_PASSWORD = "Noosfera1985"


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

driver = None

def login_into_twitter(driver, username, password):
    # navigate to login screen
    logger.info("Start login process")
    driver.get('https://twitter.com/i/flow/login')
    driver.maximize_window()
    if not wait_till_present(driver, f"{twitter_xpath_headless['username_input']}"):
        logger.error("Cannot access a usename field in login form")
        return False
    username_field = driver.find_element_by_xpath(f"{twitter_xpath_headless['username_input']}")
    username_field.send_keys(username)
    #find and clicking Next
    next = driver.find_element_by_xpath(f"{twitter_xpath_headless['login_next_button']}")
    next.click()
    if not wait_till_present(driver, f"{twitter_xpath_headless['password_input']}"):
        logger.error("Cannot access a password field in login form")
        return False
    password_field = driver.find_element_by_xpath(f"{twitter_xpath_headless['password_input']}")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    logger.info('Login succes')
    sleep(1)
    return True




def init_driver():
    logger.info("Initialization of Selenium driver")
    options = Options()
    options.headless = True
    global driver
    driver = webdriver.Firefox(options=options)
    if not login_into_twitter(driver, USER, MY_PASSWORD):
        logger.error("Cannot login into twitter")
        driver.close()
        exit(1)
    logger.info("Initialization done")

def close_driver():
    driver.close()

def get_tweets(card):
    
    # time
    time = card.find_element_by_xpath('.//time').get_attribute('datetime')
    time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000Z")

    # nickname
    try:
        element = card.find_element_by_xpath(twitter_xpath_headless["nickname"])
        parsed_nickname = ""
        for el in element.find_elements_by_xpath('./child::*'):
            if el.tag_name == "span":
                parsed_nickname += el.text
            elif el.tag_name == "img":
                parsed_nickname += el.get_attribute('alt')
            else:
                logger.warning(f"Unknown tag {el.tag_name} is presented")
    except:
        return -1
    # user tag
    try:
        user_tag = card.find_element_by_xpath(twitter_xpath_headless["user_tag"]).text
    except:
        return -1
    #text
    try:
        element = card.find_element_by_xpath(twitter_xpath_headless["text"])
        text = ""
        for el in element.find_elements_by_xpath('./child::*'):
            if el.tag_name == "span":
                text += el.text
            elif el.tag_name == "img":
                text += el.get_attribute('alt')
            else:
                logger.warning(f"Unknown tag {el.tag_name} is presented")
    except :
        text = "<no text>"
    #isRetweeted
    is_reposted = False
    try:
        card.find_element_by_xpath(twitter_xpath_headless["is_reposted"]).text
        is_reposted = True
    except :
        pass
    #img
    """ img = card.find_elements_by_xpath(f".//img")
    img_objs = []
    for im in img:
        src = im.get_attribute('src')
        if "/emoji/" in src:
            continue
        # download the image
        path = f"imgs/{uuid.uuid1()}.jpg"
        try:
            urllib.request.urlretrieve(src, path)
        except urllib.error.URLError:
            continue

        img_objs.append(Multimedia(post=current_post, type="image", path=path)) """

    return Post(text=text, is_reposted=is_reposted,  nickname=parsed_nickname, datetime=time, user_tag=user_tag, )


        



def get_twitter_user(user_id: str):
    logger.info("Entering twitter scrapper")

    if driver == None:
        raise ValueError("Selenium driver is not initialized")

    
    link = f"https://twitter.com/{user_id}"
    
    driver.get(link)
    driver.maximize_window()
    if not wait_till_present(driver, twitter_xpath_headless["header"]):
        return None

    if wait_till_present(driver, twitter_xpath_headless["is_exists"], timeout=5):
        logger.info(f"Doesn't exist or hidden: {link}")
        #user.is_exists = False
        return None

    if not wait_till_present(driver, twitter_xpath_headless["wall"]):
        logger.error(f"Can't access tweet wall on {link}")
        return None

    sleep(1)

    tweet_ids = set()
    tweets_list = []
    scrolling = True
    last_position = driver.execute_script("return window.pageYOffset;")

    logger.info(f"Start scraping of {link}")
    while scrolling:
        page_cards = driver.find_elements_by_xpath(twitter_xpath_headless["wall"])
        for card in page_cards[-15:]:
            tweet = get_tweets(card)
            if tweet == -1:
                logger.error("Something went wrong when scraping tweets. Check scrapper configuration")
                return None
            else:
                tweet_id = tweet.text + str(tweet.datetime)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    tweets_list.append(tweet)
        scrolling, last_position = scrolling_loop(driver, last_position)
        #logger.info("User defined termination")
        #break
    logger.info("Scraping complete")
    return tweets_list

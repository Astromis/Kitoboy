# from datetime import datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
# import pandas as pd
# from getpass import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import logging
from logging import StreamHandler, Formatter
import urllib.request
import uuid
# import sqlalchemy as db
from sqlalchemy.orm import Session
from models import engine
from models import Users, Multimedia, Posts
import datetime as dt

USER = "oksigeno1"
MY_PASSWORD = "Noosfera1985"

# updated 19.05.2022
class_names = {
    "head": "css-1dbjc4n r-1wbh5a2 r-dnmrzs r-1ny4l3l",
    "tweets": "css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg",
    "text": "css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0",
    "isRetweered":"css-901oao css-16my406 css-cens5h r-1bwzh9t r-poiln3 r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0",
    "nickname" : "css-901oao r-1awozwy r-1nao33i r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0",
    "user_tag":"css-901oao css-bfa6kz r-1bwzh9t r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0",
    "is_exists": "css-901oao r-1fmj7o5 r-37j5jr r-1yjpyg1 r-1vr29t4 r-ueyrd6 r-5oul0u r-bcqeeo r-fdjqy7 r-qvutc0",
    "username_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "password_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "login_next_button" : '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]',
    "user_tag_on_rel_pages" : '//div[@class="css-901oao css-cens5h r-1bwzh9t r-37j5jr r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0"]/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]'
}

# this for headless
class_names = {
    "head": "css-1dbjc4n r-1wbh5a2 r-dnmrzs r-1ny4l3l",
    "tweets": "css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg",
    "text": "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0", # data-testid
    "isRetweered":"css-901oao css-16my406 css-cens5h r-1bwzh9t r-poiln3 r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0",
    "nickname" : "css-901oao r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0",
    "user_tag":"css-901oao css-bfa6kz r-14j79pv r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0",
    #"is_exists": "css-901oao r-1fmj7o5 r-37j5jr r-1yjpyg1 r-1vr29t4 r-ueyrd6 r-5oul0u r-bcqeeo r-fdjqy7 r-qvutc0",
    "username_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "password_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "login_next_button" : '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]',
    "user_tag_on_rel_pages" : '//div[@class="css-901oao css-cens5h r-1bwzh9t r-37j5jr r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0"]/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]'
}

session = Session(bind=engine)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

logger.info("Initialization of Selenium driver")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)


def get_tweets(card, session, user):
    
    # time
    time = card.find_element_by_xpath('.//time').get_attribute('datetime')
    time = dt.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000Z")
    # FIXME
    if user.last_visited != None:
        if time < user.last_visited:
            return -1
    
    # nickname
    try:
        element = card.find_element_by_xpath(f'.//div[@class="{class_names["nickname"]}"]')
        nickname = ""
        for el in element.find_elements_by_xpath('./child::*'):
            if el.tag_name == "span":
                nickname += el.text
            elif el.tag_name == "img":
                nickname += el.get_attribute('alt')
            else:
                logger.warning(f"Unknown tag {el.tag_name} is presented")
    except:
        raise KeyError
    # user tag
    try:
        user_tag = card.find_element_by_xpath(f'.//div[@class="{class_names["user_tag"]}"]').text
    except:
        raise KeyError
    
    
    #text
    try:
        element = card.find_element_by_xpath(f'.//div[@class="{class_names["text"]}"]')
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
    isRetweeted = False
    try:
        card.find_element_by_xpath(f'.//span[@class="{class_names["isRetweered"]}"]').text
        isRetweeted = True
    except :
        pass
    current_post = Posts(text=text, is_reposted=isRetweeted, datetime=time, user=user)
    #img
    img = card.find_elements_by_xpath(f".//img")
    img_objs = []
    for im in img:
        src = im.get_attribute('src')
        if "/emoji/" in src:
            continue
        # download the image
        path = f"imgs/{uuid.uuid1()}.jpg"
        print(src)
        try:
            urllib.request.urlretrieve(src, path)
        except urllib.error.URLError:
            continue

        img_objs.append(Multimedia(post=current_post, type="image", path=path))
    session.add(current_post)
    session.add_all(img_objs)
    session.commit()
    return (text, isRetweeted, nickname, user_tag, time)

def login_into_twitter(driver):
    # navigate to login screen
    logger.info("Start login process")
    driver.get('https://twitter.com/i/flow/login')
    driver.maximize_window()
    wait_till_present(driver, f"{class_names['username_input']}")
    username = driver.find_element_by_xpath(f"{class_names['username_input']}")
    username.send_keys(USER)
    #find and clicking Next
    next = driver.find_element_by_xpath(f"{class_names['login_next_button']}")
    next.click()
    wait_till_present(driver, f"{class_names['password_input']}")
    password = driver.find_element_by_xpath(f"{class_names['password_input']}")
    password.send_keys(MY_PASSWORD)
    password.send_keys(Keys.RETURN)
    logger.info('Login succes')
    sleep(5)


def wait_till_present(driver, element, timeout=90):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, element))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        logger.info(f"Timed out waiting for page to load. Element: {element}")
        driver.close()
        
def scrolling_loop(driver, last_position):
    scroll_attempt = 0
    while True:
        # check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            # end of scroll region
            if scroll_attempt >= 3:
                return False, last_position
            else:
                sleep(2) # attempt another scroll
        else:
            last_position = curr_position
            break
    return True, last_position


def get_tweeter_user(user_id: int):
    logger.info("Entering twitter scrapper")
    
    driver.get('https://twitter.com/login')
    
    user = session.query(Users).where(Users.id == user_id).first()
    
    user_tag = user.user_tag
    link = f"https://twitter.com/{user_tag}"

        
    
    driver.get(link)
    driver.maximize_window()
    wait_till_present(driver, f'//div[@class="{class_names["head"]}"]')
    try:
        if options.headless == True:
            element_present = EC.presence_of_element_located((By.XPATH, f'//div[@class="{class_names["tweets"]}"]'))
        else:
            element_present = EC.presence_of_element_located((By.XPATH, f'//div[@class="{class_names["is_exists"]}"]'))
        WebDriverWait(driver, 5).until(element_present)
        logger.info(f"Doesn't exist or hidden: {link}")
        driver.close()
        user.is_exists = False
        session.add(user)
        session.commit()
        return 
    except TimeoutException:
        pass
    if not options.headless:
        wait_till_present(driver, f'//article[@class="{class_names["tweets"]}"]')
    sleep(5)
    data = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    logger.info("Start scraping")
    while scrolling:
        page_cards = driver.find_elements_by_xpath(f'//article[@class="{class_names["tweets"]}"]')
        for card in page_cards[-15:]:
            tweet = get_tweets(card, session, user)
            if tweet != -1:
                tweet_id = tweet[0] + str(tweet[4])
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    # data.append(tweet)
            else:
                scrolling = False
                break
                
        scrolling, last_position = scrolling_loop(driver, last_position)
        logger.info("User defined termination")
        break
    # close the web driver
    logger.info("Scraping complete")
    driver.close()
    #df = pd.DataFrame(data, columns=["text", "is_retweeted", "nickname", "user_tag", "date"])
    #df.date = df.date.apply(lambda x: pd.to_datetime(x, format="%Y-%m-%dT%H:%M:%S"))
    return #df

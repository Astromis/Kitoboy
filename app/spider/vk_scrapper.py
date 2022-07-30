import re
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .twitter_scrapper import wait_till_present, scrolling_loop
#from msedge.selenium_tools import Edge, EdgeOptions

import sys
import logging
from logging import StreamHandler, Formatter

session = None

# updated 19.05.2022
class_names_head = {
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
class_names_headless = {
    "head": "css-1dbjc4n r-1wbh5a2 r-dnmrzs r-1ny4l3l",
    "tweets": "css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg",
    "text": "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0", # data-testid
    "isRetweered":"css-901oao css-16my406 css-cens5h r-1bwzh9t r-poiln3 r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0",
    "nickname" : "css-901oao r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0",
    "user_tag":"css-901oao css-bfa6kz r-14j79pv r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0",
    "is_exists": "css-901oao r-18jsvk2 r-37j5jr r-1yjpyg1 r-1vr29t4 r-ueyrd6 r-5oul0u r-bcqeeo r-fdjqy7 r-qvutc0",
    "username_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "password_input" : '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]',
    "login_next_button" : '//div[@class="css-18t94o4 css-1dbjc4n r-sdzlij r-1phboty r-rs99b7 r-ywje51 r-usiww2 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr r-13qz1uu"]',
    "user_tag_on_rel_pages" : '//div[@class="css-901oao css-cens5h r-1bwzh9t r-37j5jr r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0"]/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]'
}

USER = '' 
MY_PASSWORD = ''

class_names = class_names_headless
# session = Session(bind=engine)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

def login_into_vk(driver, username, password):
    driver.get('https://vk.com/')
    sign_in_button = driver.find_element_by_xpath('//button[@class="FlatButton FlatButton--primary FlatButton--size-l FlatButton--wide VkIdForm__button VkIdForm__signInButton"]')
    sign_in_button.click()
    username = driver.find_element_by_xpath("//input[@class='vkc__TextField__input']") # [@name='username?']
    username.send_keys(username)
    continue_button = driver.find_element_by_xpath('//button[@class="vkc__Button__container vkc__Button__primary vkc__Button__fluid"]')
    continue_button.click()
    password = driver.find_element_by_xpath("//input[@class='vkc__TextField__input'][@name='password']")
    password.send_keys(password)
    continue_button = driver.find_element_by_xpath('//button[@class="vkc__Button__container vkc__Button__primary vkc__Button__fluid"]')
    continue_button.click()
    # otp = driver.find_element_by_xpath("//input[@class='vkc__TextField__input'][@name='otp']")
    # otp.send_keys()

logger.info("Initialization of Selenium driver")
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
if not login_into_vk(driver, USER, MY_PASSWORD):
    logger.error("Cannot login into twitter")
    driver.close()
    #session.close()
    exit(1)


def get_posts(post):
    image_src_list = []
    audio_list = []

    try:
        author_info = post.find_element_by_xpath("//a[@class='author']")
        tag = author_info.get_attribute("href")
        nickname = author_info.text
        time = post.find_element_by_class_name("post_date").text
    except:
        return -1
    try:
        text = post.find_element_by_class_name("wall_post_text").text
    except:
        text = "<no text>"
    try:
        image_link_list = post.find_element_by_xpath("//div[@class='page_post_sized_thumbs  clear_fix']")
        image_link_list = [x for x in image_link_list.find_elements_by_xpath("a")]
    except:
        pass
    else:
        for image_link in image_link_list:
            image_link.click()
            image_src_list.append(driver.find_element_by_id("pv_photo").find_element_by_xpath("img").get_attribute("src"))
            driver.find_element_by_xpath("//div[@class='pv_close_btn']").click()
    try:
        audio_components = post.find_element_by_xpath(".//div[@class='wall_audio_rows _wall_audio_rows PostMediaRowWithActionStatusBarSeparator']")
        audio_components = audio_components.find_elements_by_xpath("./div")
    except:
        pass
    else:
        for aud in audio_components:
            perfonacer = aud.find_element_by_xpath(".//div[@class='audio_row__performers']").text
            title = aud.find_element_by_xpath(".//div[@class='audio_row__title _audio_row__title']").text
            audio_list.append((perfonacer, title))
    return (tag, nickname, time, text, image_src_list, audio_list)


def get_vk_user(user_id: int):
    logger.info("Entering vk scrapper")

    user = session.query(Users).where(Users.id == user_id).first()
    
    user_tag = user.user_tag
    link = f"https://vk.com/{user_tag}"
    
    driver.get(link)
    driver.maximize_window()
    if not wait_till_present(driver, f'//div[@class="{class_names["head"]}"]'):
        return False

    if wait_till_present(driver, f'//div[@class="{class_names["is_exists"]}"]', timeout=5):
        logger.info(f"Doesn't exist or hidden: {link}")
        user.is_exists = False
        session.add(user)
        session.commit()
        return True

    if not wait_till_present(driver, f'//article[@class="{class_names["tweets"]}"]'):
        logger.error(f"Can't access tweets on {link}")
        return False

    sleep(1)

    vk_post_ids = set()
    scrolling = True
    last_position = driver.execute_script("return window.pageYOffset;")

    logger.info(f"Start scraping of {link}")
    while scrolling:
        page_cards = driver.find_elements_by_xpath(f'//div[@id="page_wall_posts"]')
        for card in page_cards[-15:]:
            post = get_posts(card, session, user)
            if post == 0:
                scrolling = False
                break
            elif post == -1:
                logger.error("Something went wrong when scraping tweets. Check configuration")
                return False
            else:
                post_id = post[0] + str(post[4])
                if post_id not in vk_post_ids:
                    vk_post_ids.add(post_id)
        scrolling, last_position = scrolling_loop(driver, last_position)
        #logger.info("User defined termination")
        #break
    logger.info("Scraping complete")
    return True

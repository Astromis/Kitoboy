from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import pandas as pd
from getpass import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

USER = "oksigeno1"
MY_PASSWORD = "Noosfera1985"

class_name = {
    "tweets": "css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg",
    "text": "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0",
    "isRetweered":"css-901oao css-16my406 css-cens5h r-14j79pv r-poiln3 r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0",
    "nickname" : "css-901oao css-bfa6kz r-1awozwy r-18jsvk2 r-6koalj r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0",
    "user_tag":"css-901oao css-bfa6kz r-14j79pv r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"
    
}

def get_tweets(card):
    #text
    try:
        element = card.find_element_by_xpath(f'.//div[@class="{class_name["text"]}"]')
        text = ""
        for el in element.find_elements_by_xpath('./child::*'):
            if el.tag_name == "span":
                text += el.text
            elif el.tag_name == "img":
                text += "<emoji>"+el.get_attribute('title')+"</emoji>"
            else:
                print(f"WARNING! Unknown tag {el.tag_name} is presented")
    except :
        text = "<no text>"
    #isRetweeted
    isRetweeted = False
    try:
        card.find_element_by_xpath(f'.//span[@class="{class_name["isRetweered"]}"]').text
        isRetweeted = True
    except :
        pass
    # nickname
    try:
        element = card.find_element_by_xpath(f'.//div[@class="{class_name["nickname"]}"]')
        nickname = ""
        for el in element.find_elements_by_xpath('./child::*'):
            if el.tag_name == "span":
                nickname += el.text
            elif el.tag_name == "img":
                nickname += "<emoji>"+el.get_attribute('title')+"</emoji>"
            else:
                print(f"WARNING! Unknown tag {el.tag_name} is presented")
    except:
        nickname = "<no nickname>"
    # user tag
    try:
        user_tag = card.find_element_by_xpath(f'.//div[@class="{class_name["user_tag"]}"]').text
    except:
        user_tag = "<no user_tag>"
    # time
    time = card.find_element_by_xpath('.//time').get_attribute('datetime')
    return (text, isRetweeted, nickname, user_tag, time)

def get_tweeter_user(link: str):

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get('https://twitter.com/login')
    '''
    while True:
        try:
            username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
            username.send_keys(USER)
            password = driver.find_element_by_xpath('//input[@name="session[password]"]')
            password.send_keys(MY_PASSWORD)
            password.send_keys(Keys.RETURN)
            sleep(1)
            break
        except NoSuchElementException:
            continue
    
    '''
    driver.get(link)
    driver.maximize_window()
    data = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    while scrolling:
        page_cards = driver.find_elements_by_xpath(f'//article[@class="{class_name["tweets"]}"]')
        for card in page_cards[-15:]:
            tweet = get_tweets(card)
            if tweet:
                tweet_id = tweet[0] + tweet[4]
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                
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
                    scrolling = False
                    break
                else:
                    sleep(2) # attempt another scroll
            else:
                last_position = curr_position
                break

    # close the web driver
    driver.close()
    df = pd.DataFrame(data, columns=["text", "is_retweeted", "nickname", "user_tag", "date"])
    df.date = df.date.apply(lambda x: pd.to_datetime(x, format="%Y-%m-%dT%H:%M:%S"))
    return df

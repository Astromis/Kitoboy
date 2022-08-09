
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from .common import wait_till_present, scrolling_loop
from .data_model import Multimedia, Post
from getpass import getpass
import sys
import logging
from logging import StreamHandler, Formatter
from .scrapper_config import vk_xpath_headless


USER = 'aarmaageedoon@yandex.ru' 
MY_PASSWORD = '4611116003Igor'

driver = None

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

def login_into_vk(driver, username, password):
    driver.get('https://vk.com/')
    
    username_field = driver.find_element_by_xpath(vk_xpath_headless["username_input"]) 
    username_field.send_keys(username)
    sign_in_button = driver.find_element_by_xpath('//button[@class="FlatButton FlatButton--primary FlatButton--size-l FlatButton--wide VkIdForm__button VkIdForm__signInButton"]')
    sign_in_button.click()
    wait_till_present(driver, vk_xpath_headless["password_input"])
    password_field = driver.find_element_by_xpath(vk_xpath_headless["password_input"])
    password_field.send_keys(password)
    continue_button = driver.find_element_by_xpath('//button[@class="vkc__Button__container vkc__Button__primary vkc__Button__fluid"]')
    continue_button.click()
    wait_till_present(driver, vk_xpath_headless["otp_input"])
    otp = driver.find_element_by_xpath(vk_xpath_headless["otp_input"])
    otp.send_keys(getpass())
    continue_button = driver.find_element_by_xpath('//button[@class="vkc__Button__container vkc__Button__primary vkc__Button__fluid"]')
    continue_button.click()
    wait_till_present(driver, "//div[@class='LeftMenu__icon']")
    return True

def init_driver():
    logger.info("Initialization of Selenium driver")
    options = Options()
    options.headless = True
    global driver
    driver = webdriver.Firefox(options=options)
    if not login_into_vk(driver, USER, MY_PASSWORD):
        logger.error("Cannot login into twitter")
        driver.close()
        exit(1)
    logger.info("Initialization done")


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
    """ try:
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
            audio_list.append((perfonacer, title)) """
    

    return Post(text=text, is_reposted=False, nickname=nickname, user_tag=tag, datetime=time)


def get_vk_user(user_id: str):
    logger.info("Entering vk scrapper")

    if driver == None:
        raise ValueError("Selenium driver is not initialized")
    
    link = f"https://vk.com/{user_id}"
    
    driver.get(link)
    driver.maximize_window()
    if not wait_till_present(driver, vk_xpath_headless["wall"]):
        return None

    """ if wait_till_present(driver, f'//div[@class="{class_names["is_exists"]}"]', timeout=5):
        logger.info(f"Doesn't exist or hidden: {link}")
        #user.is_exists = False
        return None

    if not wait_till_present(driver, f'//article[@class="{class_names["tweets"]}"]'):
        logger.error(f"Can't access tweets on {link}")
        return False """

    sleep(1)

    vk_post_ids = set()
    scrolling = True
    last_position = driver.execute_script("return window.pageYOffset;")
    post_list = []
    logger.info(f"Start scraping of {link}")
    while scrolling:
        page_posts = driver.find_elements_by_xpath(vk_xpath_headless["wall"])
        for next_post in page_posts[-15:]:
            post = get_posts(next_post)
            if post == -1:
                logger.error("Something went wrong when scraping tweets. Check scrapper configuration")
                return False
            else:
                post_id = post.user_tag + str(post.datetime)
                if post_id not in vk_post_ids:
                    vk_post_ids.add(post_id)
                    post_list.append(post)
        scrolling, last_position = scrolling_loop(driver, last_position)
        #logger.info("User defined termination")
        #break
    logger.info("Scraping complete")
    return post_list

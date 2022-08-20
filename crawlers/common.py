from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

def wait_till_present(driver, element, timeout=90):
    try:
        logger.info(f"Waiting for {element}")
        element_present = EC.presence_of_element_located((By.XPATH, element))
        WebDriverWait(driver, timeout).until(element_present)
        return True
    except TimeoutException:
        logger.warn(f"Timed out waiting for page to load. Element: {element}")
        return False

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
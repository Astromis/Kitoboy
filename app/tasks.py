from .app import celery_instance
#from .spider.twitter_scrapper import get_tweeter_user
#from .spider.vk_scrapper import get_vk_user

from subprocess import Popen

@celery_instance.task
def scrape_twitter(id: int):
    return get_tweeter_user(id)

@celery_instance.task
def scrape_telegram(char_url):
    p = Popen(["python", "app/spider/telegram_scrapper.py", char_url], shell=False)
    p.communicate()

@celery_instance.task
def scrape_vk(id: int):
    return get_vk_user(id)
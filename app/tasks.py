from .app import celery
from datetime import datetime
# from subprocess import Popen

# from .crawlers.twitter_scrapper import get_tweeter_user
# from .crawlers.vk_scrapper import get_vk_user



# @celery.task
# def scrape_twitter(id: int):
#     return get_tweeter_user(id)
#
# @celery.task
# def scrape_telegram(char_url):
#     p = Popen(["python", "app/crawlers/telegram_scrapper.py", char_url], shell=False)
#     p.communicate()
#
# @celery.task
# def scrape_vk(id: int):
#     return get_vk_user(id)


@celery.task
def task_1():
    return f'The task run every minute {datetime.now()}'


@celery.task
def task_2():
    return f'The task run every two minutes {datetime.now()}'

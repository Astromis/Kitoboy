"""tasks.py"""
# pylint: disable=W0613
import json
import requests as rq
from celery.schedules import crontab

from project.jobs import make_celery, API_KEY

celery_app = make_celery()


@celery_app.task(bind=True)
def weather_forecast(self, zip_code):
    '''
    get weather forecast for the area with provided zip code
    :zip_code: zip code of the area where the weather forecast is checked
    '''
    url = 'http://api.weatherapi.com/v1/forecast.json?' + \
          f'key={API_KEY}&q={zip_code}&days=7'
    res = json.loads(rq.get(url).text)
    weather = {'current':{}, 'forecast':[]}
    weather['current']['last_updated'] = res['current']['last_updated']
    weather['current']['condition'] = res['current']['text']
    weather['current']['temp_c'] = res['current']['temp_c']
    weather['current']['wind_mph'] = res['current']['wind_mph']
    weather['current']['humidity'] = res['current']['humidity']
    for day_res in res['forecast']['forecastday']:
        day_weather = {}
        day_weather['maxtemp_c'] = day_res['day']['maxtemp_c']
        day_weather['mintemp_c'] = day_res['day']['mintemp_c']
        day_weather['avgtemp_c'] = day_res['day']['avgtemp_c']
        day_weather['maxwind_mph'] = day_res['day']['maxwind_mph']
        day_weather['avghumidity'] = day_res['day']['avghumidity']
        day_weather['conidition'] = day_res['day']['condition']['text']
        weather['forecast'].append(day_weather)
    return weather

@celery_app.task(bind=True)
def current_weather(self, city):
    '''
    check the current weather for the provided city
    :city: the name of the city where current weather is checked
    '''
    url = 'http://api.weatherapi.com/v1/current.json?' + \
          f'key={API_KEY}&q={city}'
    res = json.loads(rq.get(url).text)
    weather = {}
    weather['last_updated'] = res['current']['last_updated']
    weather['condition'] = res['current']['condition']['text']
    weather['temp_c'] = res['current']['temp_c']
    weather['wind_mph'] = res['current']['wind_mph']
    weather['humidity'] = res['current']['humidity']
    return weather


@celery_app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    '''
    schedule two recurring tasks:
      1. check current weather once every 10 seconds
      2. check weather forecast every Monday morning 7:30am
    :sender (Any): the sender of the signal. Either a specific object
                   or :const:`None`.
    '''
    # Checking weather information every 10 seconds
    sender.add_periodic_task(10.0, current_weather.s('Los Angeles'))

    # Executes every Monday morning at 7:30 am
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        weather_forecast.s('90717'),
    )

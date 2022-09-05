import requests
import json
from pprint import pprint

# TODO я тут ничего не проверял, но увидел, что ты пытаешься парсить json,
#  так вот есть крутая библиотека для этого - beautifullsoup и вопросы по импортам,
#  ты импортировал библиотеки, но не использовал их - так не надо

token = '5154079349:AAFzD7ZvnbV2WWgPZqe9512qS7vucaXvfis'
i = 0

while True:
    result = requests.get('http://api.telegram.org/bot'+token+'/getUpdates',
                          params={'offset': i + 1})
    data = result.json()
    for update in data['result']:
        i = update['update_id']
        chat_id = update['message']['chat']['id']
        user_text = update['message']['text']
        if user_text == 'Новости' :
            url = ('http://newsapi.org/v2/top-headlines?'
                   'country=ru&'
                   'apiKey=02dd48216b094faa9de5a15da15f8ba4')
            news_result = requests.get(url)
            news_data = news_result.json()
            for news_update in news_data['articles']:
                last_news = news_update['title']
                send_news = requests.get(
                    'https://api.telegram.org/bot'+token+'/sendMessage',
                    params={'chat_id': chat_id, 'text': last_news})
            send_result = requests.get(
                'https://api.telegram.org/bot'+token+'/sendMessage',
                params={'chat_id': chat_id,
                        'text': 'Введите "погода" для получения текущей погоды\nВведите "новости" для получения '
                                'последних новостей из России'})
        elif user_text == 'погода':
            send_result = requests.get(
                'https://api.telegram.org/bot'+token+'/sendMessage',
                params={'chat_id': chat_id, 'text': 'Укажите название города'})
            my_result = []
            while True :
                my_result = requests.get('http://api.telegram.org/bot'+token+'/getUpdates', params={'offset': i + 1})
                my_data = my_result.json()
                city_name = ''
                for city_update in my_data['result']:
                    i = city_update['update_id']
                    city_name = city_update['message']['text']
                if city_name=="" : continue
                weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + str(city_name) + \
                              '&units=metric&lang=ru&appid=7d9ee308f1f7c1ad06bf9ccb1abbf0ae'
                weather_result = requests.get(weather_url)
                weather_data = weather_result.json()
                for weather_update in weather_data['weather']:
                    last_weather = weather_update['description']
                    send_weather = requests.get('https://api.telegram.org/bot'+token+'/sendMessage',
                                                params={'chat_id': chat_id, 'text': last_weather})
                send_weather = requests.get(
                    'https://api.telegram.org/bot'+token+'/sendMessage',
                    params={'chat_id': chat_id, 'text': 'Температура ' + str(weather_data['main']['temp']) + ' C'})
                send_weather = requests.get(
                    'https://api.telegram.org/bot'+token+'/sendMessage',
                    params={'chat_id': chat_id, 'text': 'Ветер ' + str(weather_data['wind']['speed']) + ' м/с'})
                send_weather = requests.get(
                    'https://api.telegram.org/bot'+token+'>/sendMessage',
                    params={'chat_id': chat_id, 'text': 'Влажность ' + str(weather_data['main']['humidity']) + ' %'})
                send_result = requests.get(
                    'https://api.telegram.org/bot'+token+'/sendMessage',
                    params={'chat_id': chat_id, 'text': 'Введите "погода" для получения текущей погоды\nВведите '
                                                        '"новости" для получения последних новостей из России'})
                break
        else:
            send_result = requests.get(
                'https://api.telegram.org/bot'+token+'/sendMessage',
                params={'chat_id': chat_id, 'text': 'Введите "погода" для получения текущей погоды\nВведите '
                                                    '"новости" для получения последних новостей из России'})
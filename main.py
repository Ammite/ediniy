import flask
import constants
from flask import Flask
from flask import request
from flask import jsonify
import constants
import re
import telebot
import requests
import json
import sql
import os

# from flask_sslify import SSLify

app = Flask(__name__)
URL = constants.URLc

if_in_contacts = False
login = False
passwd = False
login_that_uses = ''
passwd_that_uses = ''


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_updates():
    url = URL + 'getUpdates'
    r = requests.get(url)
    return r.json()


def send_message(chat_id, text='', parse_mode='Markdown'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
    r = requests.post(url, json=answer)
    return r.json()


def send_location(chat_id, lat, lon):
    url = URL + 'sendLocation'
    answer = {'chat_id': chat_id, 'latitude': lat, 'longitude': lon}
    r = requests.post(url, json=answer)
    return r.json()


def city(chat_id, message):
    lib = constants.library_of_places[message]
    send_message(chat_id, "Город: {} \nАдрес: {}\nНомера: {}, {}\nНа карте:"
                 .format(lib['city'], lib['address'], lib['number1'], lib['number2']))
    send_location(chat_id, lib['coor_lat'], lib['coor_lon'])


def news(chat_id):
    send_message(chat_id, "Канал новостей компании \"Единый Выбор\": @ediniyvibornews")


def programs(chat_id):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': 'Выберите программу.',
              'reply_markup': {"keyboard": [["50 нa 50"], ["Сeмья"], ["Нaзaд"]]}}
    r = requests.post(url, json=answer)
    return r.json()


def programs_data(chat_id, message):
    if message == "Сeмья":
        send_message(chat_id,
                     "Срок получения, месяцев: {}\nПервоначальный взнос  от стоимости квартиры, %: {}\nСрок рассрочки, лет: {}\nЦелевой взнос, %: {}".format(
                         "6-12", "25", "до 9", "2"))
    if message == "50 нa 50":
        send_message(chat_id,
                     "Срок получения, месяцев: {}\nПервоначальный взнос  от стоимости квартиры, %: {}\nСрок рассрочки, лет: {}\n".format(
                         "3-6", "50", "до 9"))


def work_with_text():
    r = request.get_json()
    global if_in_contacts
    global login
    global passwd
    chat_id = r['message']['chat']['id']
    if 'text' in r['message']:
        message = r['message']['text']
    else:
        message = ''
    print(chat_id, message)
    if login and is_number(message):
        take_data(chat_id, message)

    elif message == '/menu' or message == "Нaзaд" or message == "/start":
        if_in_contacts = False
        summon_menu(chat_id)

    elif message == "Контакты":
        contacts(chat_id)

    elif message == "Новости":
        news(chat_id)

    elif message == "Программы на получение недвижимости":
        programs(chat_id)

    elif message == "50 нa 50" or message == "Сeмья":
        programs_data(chat_id, message)

    elif message in constants.cities:
        city(chat_id, message)

    elif message == "Вопрос-ответ":
        send_message(chat_id, "Ознакомить можно [тут](http://first-kz.kz/index.php#Layer17)", 'Markdown')

    elif message == 'Личный кабинет':
        open_sing_in_payers(chat_id)

    elif message == 'Вoйти в кабинет очереди':  # Useful
        pass

    elif message == 'Вoйти в кабинет пайщика':  # Useful
        open_sing_in_payers(chat_id)

    elif message in constants.library_of_funcs:
        send_message(chat_id, "[WIP]\nЕще не работает.")

    else:
        send_message(chat_id, "Не понимаю введенные данные")


def take_data(chat_id, message):
    sql.take_data_from_db(chat_id, message)


def is_number(message):
    if len(message) == 11 or len(message) == 12:
        if message[:-10] == '+7':
            if ('8' + message[2:]).isdigit():
                return True
            else:
                return False


def open_sing_in_payers(chat_id):
    global login
    login = True
    send_message(chat_id, 'Введите логин в формате:\n"(ваш номер)".\n'
                          'Пример:"87071212123"')


def open_cabinet(chat_id):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': 'Выберите программу.',
              'reply_markup': {"keyboard": [["Вoйти в кабинет очереди"], ["Вoйти в кабинет пайщика"], ["Нaзaд"]]},
              'one_time_keyboard': 'true'}
    r = requests.post(url, json=answer)
    return r.json()


def parser(pattern, message):
    if pattern in message:
        return True
    else:
        return False


def contacts(chat_id):
    global if_in_contacts
    if_in_contacts = True
    send_message(chat_id, "Наши контакты [тут](http://first-kz.kz/#Layer16)")


def summon_menu(chat_id):
    # user_markup = telebot.types.ReplyKeyboardMarkup()
    url = URL + 'sendMessage'
    # name = "amas"
    answer = {'chat_id': chat_id, 'text': 'Главное меню.', 'reply_markup': {"keyboard": constants.array_of_arrays}}
    r = requests.post(url, json=answer)
    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        work_with_text()
        # write_json(r)
        # return jsonify(r)
    return '<h1>Testing Flask!!!!</h1>'


def main():
    pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

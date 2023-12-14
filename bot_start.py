from urllib.parse import urljoin

import requests
import time
import telebot
from telebot import types
import threading
from bs4 import BeautifulSoup

bot = telebot.TeleBot('5825193393:AAFmktYEBi_aTilQdrvIY493NliAdm4Yb7U')


#получение юрл


def get_schedule_image_url():
    url = 'http://sch17petrozavodsk.narod.ru/new_news/rasp1.htm'  # Адрес страницы с расписанием в виде картинки
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('img', {'class': 'featurette-image img-responsive center-block'})
    if img_tag:
        img_url = img_tag['src']
        img_url = urljoin(url, img_url)
        return img_url
    return None


#Получение картинки


def get_schedule():
    img_url = get_schedule_image_url()
    if img_url:
        response = requests.get(img_url)
        img_content = response.content
        with open('schedule.png', 'wb') as f:
            f.write(img_content)
        return True
    return False


#само расписание


@bot.message_handler(commands=['sch'])
def send_schedule_image(message):
    schedule = get_schedule()
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn = types.KeyboardButton('Узнать расписание!')
    # markup.add(btn)
    if schedule:
        img_url = get_schedule_image_url()
        response = requests.get(img_url)
        img_content = response.content
        bot.send_photo(chat_id=message.chat.id, photo=img_content)
    else:
        bot.reply_to(message, 'К сожалению, расписание в данный момент недоступно.')


#Старт


@bot.message_handler(commands=['start'])
def Privet(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ras = types.KeyboardButton('Узнать расписание!')

    markup.add(ras)

    bot.send_message(message.chat.id, "Привет, подсказать расписание?", reply_markup= markup)


#Записываем id, даем рассылку


joinedFile = open("C:\schBot\id.txt", 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

#Рассылка при запуске

def mess1():
    img_url = get_schedule_image_url()
    response = requests.get(img_url)
    img_content = response.content
    for user in joinedUsers:
        bot.send_photo(user, photo=img_content)

@bot.message_handler(commands = ['podspis'])
def startJoin(message):
        if not str(message.chat.id) in joinedUsers:
            bot.reply_to(message, 'Вы подписались на обновления расписания.')
            joinedFile = open('C:\schBot\id.txt', 'a')
            joinedFile.write(str(message.chat.id) + '\n')
            joinedUsers.add(message.chat.id)
        else:
            bot.reply_to(message, 'Вы уже подписаны на обновления расписания.')


#рассылка командой


@bot.message_handler(commands = ['ras'])
def mess(message):
    img_url = get_schedule_image_url()
    response = requests.get(img_url)
    img_content = response.content
    for user in joinedUsers:
        bot.send_photo(user, photo=img_content)


#кнопка подписки


@bot.message_handler(content_types=['text'])
def PodpisBtn(message):
    flag = 0
    schedule = get_schedule()
    if schedule:
        if message.text == 'Узнать расписание!':
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
            pod = types.KeyboardButton('Подписаться!')
            markup1.add(pod)
            img_url = get_schedule_image_url()
            response = requests.get(img_url)
            img_content = response.content
            bot.send_photo(chat_id=message.chat.id, photo=img_content, reply_markup=markup1)
            bot.send_message(message.chat.id, "Подписаться на рассылку?")
    if message.text  == "Подписаться!":
        if not str(message.chat.id) in joinedUsers:
            flag = 1
            joinedFile = open('C:\schBot\id.txt', 'a')
            joinedFile.write(str(message.chat.id) + '\n')
            joinedUsers.add(message.chat.id)

        else:
            flag = 0
        if flag == 1:
            bot.reply_to(message, 'Вы подписались на обновления расписания.')
        else:
            bot.reply_to(message, 'Вы уже подписаны на обновления расписания.')


# def send_updates():
#     print("send_updates started")
#     while True:
#         schedule = get_schedule()
#         # new_url = get_schedule_image_url()
#         # flag = True
#         # if flag:
#         #     response = requests.get(new_url)
#         #     new_img_content = response.content
#         #     with open('schedule1.png', 'wb') as f1:
#         #         f1.write(new_img_content)
#         if schedule:
#             with open('schedule.png', 'rb') as f:
#                 img_content = f.read()
#             # with open("schedule1.png","rb") as f1:
#             #     new_img_content = f1.read()
#             # if new_img_content != img_content:
#             #     img_content =new_img_content
#             # else:
#                 for chat_id in chat_ids:
#                     bot.send_photo(chat_id, photo=img_content)
#         time.sleep(1440) # Проверять расписание


# Запускаем отдельный поток для отправки обновлений расписания


# t = threading.Thread(target=send_updates)
# t.start()


# Запускаем бота


print('Красава, бот работает)')
mess1()
bot.polling(none_stop=True)

import argparse
import os
import telebot
from telebot import types

from flask import Flask, request

API_TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(API_TOKEN)

server = Flask(__name__)
TELEBOT_URL = 'telebot_webhook/'
BASE_URL = 'https://badwordsbot.herokuapp.com/'

worker_dict=dict()

class Worker():
    def __init__(self, name):
        self.name = name
        self.word = None


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "Привет! Я бот, который собирает статистику матерщинников ФАО😜"
    bot.reply_to(message, text)

#Handle '/help'
@bot.message_handler(commands=['help'])
def send_explanation(message):
    text = "Чтобы сделать то-то и то-то, сделай вот это вот."
    bot.reply_to(message, text)

@bot.message_handler(commands=['test'])
def ask_who(message):
    text = "Кто провинился?"
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Костя')
    itembtn2 = types.KeyboardButton('Света')
    itembtn3 = types.KeyboardButton('Катя')
    itembtn4 = types.KeyboardButton('Дима')
    itembtn5 = types.KeyboardButton('Маша')
    itembtn6 = types.KeyboardButton('Юля')
    itembtn7 = types.KeyboardButton('Богдан')
    itembtn8 = types.KeyboardButton('Ваня')
    itembtn9 = types.KeyboardButton('Марина')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)
    msg = bot.send_message(chat_id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, what_word)

def what_word(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Бл**ь')
    itembtn2 = types.KeyboardButton('П**да')
    itembtn3 = types.KeyboardButton('Х*й')
    itembtn4 = types.KeyboardButton('Е**ть')
    itembtn5 = types.KeyboardButton('П*дар')
    chat_id = message.chat.id
    worker = Worker(message.text)
    worker_dict[chat_id] = worker
    markup.row(itembtn1,itembtn2,itembtn3)
    markup.row(itembtn4,itembtn5)
    msg = bot.send_message(chat_id, "А что сказал?")
    bot.register_next_step_handler(msg, db_writer)

def db_writer(message):
    chat_id = message.chat.id
    worker=worker_dict[chat_id]
    worker.word = message.text
    bot.send_message(chat_id, f"Матерщинник - {worker.name}, слово - {worker.word}")


@server.route('/' + TELEBOT_URL + API_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BASE_URL + TELEBOT_URL + API_TOKEN)
    return "!", 200


parser = argparse.ArgumentParser(description='Run the bot')
parser.add_argument('--poll', action='store_true')
args = parser.parse_args()

if args.poll:
    bot.remove_webhook()
    bot.polling()
else:
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    webhook()
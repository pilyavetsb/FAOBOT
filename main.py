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
    text = "Ну тут вопросик"
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Коннор')
    itembtn2 = types.KeyboardButton('Роннок')
    markup.add(itembtn1,itembtn2)
    msg = bot.send_message(chat_id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, process_choice)

def process_choice(message):
    bot.reply_to(message, f'Ты выбрал{message.text}')

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
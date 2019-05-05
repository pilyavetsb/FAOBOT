import argparse
import os
import telebot

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
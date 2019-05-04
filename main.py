import argparse
import os
import telebot

from flask import Flask, request

API_TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(API_TOKEN)

server = Flask(__name__)
TELEBOT_URL = 'telebot_webhook/'
BASE_URL = 'https://example-telebot.herokuapp.com/'


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
@@ -18,4 +23,20 @@ def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling()
@server.route('/' + TELEBOT_URL + API_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


parser = argparse.ArgumentParser(description='Run the bot')
parser.add_argument('--poll', action='store_true')
args = parser.parse_args()

if args.poll:
    bot.remove_webhook()
    bot.polling()
else:
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    bot.remove_webhook()
    bot.set_webhook(url=BASE_URL + TELEBOT_URL + API_TOKEN)
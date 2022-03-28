#general imports
import logging
from uuid import uuid4
from requests import api
from requests.models import encode_multipart_formdata
from api import token, chat_id

#Flask imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests

#Telegram imports
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler, InlineQueryHandler


#Internal files imports
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# load_dotenv(".env")
TOKEN = token
CHAT_ID = chat_id
bot = Bot(TOKEN)


TEXT = 'Hello World'
bot.send_message(CHAT_ID, TEXT)

# def listener(messages):
#     #This gests triggered when a new message gets sent to telebot
#     text = 'Message has been received!'
#     for m in messages:
#         print(m.chat.id)
#         bot.send_message(m.chat.id, text)

#     return 'Success'

#When user first starts their message
def start_msg(update: Update, context: CallbackContext):
    update.message.reply_text('Hey there! Welcome to WeatherBot! Just start by typing /start in the chat!')

#When user clicks start on Message
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hey there! Thank you for using Printo!")
    tele_id = update.message.chat.id #TODO: Update requestor database with new teleid

#TODO: FOR  REQUESTOR: update requestor when their request has been accepted
def update_requestor():


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
 
    updater.start_polling()

    # run the bot until interrupted (e.g. using Ctrl + c)
    updater.idle()

if __name__ == '__main__':
    main()

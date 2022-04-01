#general imports
import logging
from uuid import uuid4
from requests import api
from requests.models import encode_multipart_formdata
from api import token, chat_id, puja_id

#Flask imports
from flask import Flask, request as req, jsonify
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
bot = Bot(TOKEN)



#When user first starts their message
def start_msg(update: Update, context: CallbackContext):
    update.message.reply_text('Hey there! Welcome to Printo! Just start by typing /start in the chat to get your Chat ID and proceed to update it in your application!!')
    tele_id = update.message.chat.id #TODO: Update requestor database with new teleid

    return tele_id

#When user clicks start on Message
def start(update: Update, context: CallbackContext):
    tele_id = update.message.chat.id #TODO: Update requestor database with new teleid
    print(tele_id)
    update.message.reply_text(
f"""Hello! Thank you for using Printo! 
You will be able to view you requests here. 
Additionally, you'll receive updates when your active requests have been accepted!
\nPlease take note of your Chat ID: {tele_id}. \nPlease input this Chat ID in the application to get regular updates on your print requests!"""
    )
    return tele_id


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
 
    updater.start_polling()

    # run the bot until interrupted (e.g. using Ctrl + c)
    updater.idle()

if __name__ == "__main__":
    main()



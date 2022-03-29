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
CHAT_ID = chat_id
bot = Bot(TOKEN)


TEXT = 'Hello World'
# bot.send_message(CHAT_ID, TEXT)
# bot.send_message(182604325, "HELLO HOW R U? DON'T BOTHER REPLYING I CANNOT SEE IT.")

#When user first starts their message
def start_msg(update: Update, context: CallbackContext):
    update.message.reply_text('Hey there! Welcome to WeatherBot! Just start by typing /start in the chat!')
    tele_id = update.message.chat.id #TODO: Update requestor database with new teleid
    print(tele_id)
    return tele_id

#When user clicks start on Message
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
"""Hello! Thank you for using Printo! 
You will be able to view you requests here. 
    Additionally, you'll receive updates when your active requests have been accepted!"""
    )
    tele_id = update.message.chat.id #TODO: Update requestor database with new teleid
    print(tele_id)
    return tele_id



#TODO: FOR  REQUESTOR: update requestor when their request has been accepted.
#TODO: Change code to take in **data from where ever
@app.route('/update_requestor', methods=['POST'])
def update_requestor():
    #UNCOMMENT LATER - Data that is passed should be ALL provider, request and requestor details
    # data = req.get_json()
    #CHAT_ID = data['tele_id']

    bot.send_message(
        CHAT_ID, f"""A provider has accepted your request! \Provider details are as follows: 
        \nRequest ID: 1
        \nProvider Name: Arthur Hain 
        \nProvider ID: 1
        \nProvider Location: Toa Payoh
        \nProvider Telegram: @ArthurHain
        \n
        \nDetails of your print requests is as follows:
        \nColor: Black
        \nCopies: 21
        \nSide: Single
        \nSize: A4
        \nComments: Nil"""
        )
    return {"code": 200,
"request_id": 1, "provider_id":1}



#TODO: FOR  PROVIDER: update requestor when their request has been accepted.
#TODO: Change code to take in **data from where ever
@app.route('/update_provider', methods=['POST'])
def update_provider():
    #UNCOMMENT LATER - Data that is passed should be ALL provider, request and requestor details
    # data = req.get_json()
    #CHAT_ID = data['tele_id']

    bot.send_message(
        CHAT_ID, f"""A provider has accepted your request! \Provider details are as follows: 
        \nRequest ID: 1
        \nRequetor Name: Arthur Hain 
        \nRequestor ID: 1
        \nRequestor Location: Toa Payoh
        \nRequestor Telegram: @ArthurHain
        \n
        \nDetails of the accepted print requests is as follows:
        \nColor: Black
        \nCopies: 21
        \nSide: Single
        \nSize: A4
        \nComments: Nil"""
        )

    return {"code": 200, "request_id": 1, "provider_id":1}


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
 
    updater.start_polling()

    # run the bot until interrupted (e.g. using Ctrl + c)
    updater.idle()

if __name__ == "__main__":
    # app.run(port=5010, debug=True)
    main()


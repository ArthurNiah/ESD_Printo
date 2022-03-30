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
# CHAT_ID = chat_id
bot = Bot(TOKEN)



TEXT = 'Hello World'
x = {
    "request": {
        "request_id": 1,
        "requestor_id":1, 
        "provider_id":1,
        "document_id": "xxx", 
        "location_name": "Toa Payoh", 
        "color": "black",
        "no_of_copies":1, 
        "single_or_double":"single", 
        "size": "A4", 
        "comments":"MAMAMIA"
    }, 
    "requestor":{
        "requestor_id": 1,
        "first_name":"Arthur",
        "last_name":"Hain",
        "tele_id": "@ArthurHain", 
        "chat_id": "853733285"
    },
    "provider":{
        "provider_id": 1,
        "first_name":"Ruthra",
        "last_name":"Niah",
        "tele_id": "@ArthurHain",
        "chat_id":"853733285", 
        "location_name": ""
    }
}

# bot.send_message(CHAT_ID, TEXT)
# bot.send_message(182604325, "HELLO HOW R U? DON'T BOTHER REPLYING I CANNOT SEE IT.")

#When user first starts their message
#TODO: FOR  REQUESTOR: update requestor when their request has been accepted.
#TODO: Change code to take in **data from where ever
@app.route('/update_requestor', methods=['POST'])
def update_requestor():
    #UNCOMMENT LATER - Data that is passed should be ALL provider, request and requestor details
    data = req.get_json()
    CHAT_ID = data['provider']['chat_id']


    bot.send_message(CHAT_ID, "Testing")

    try:
        bot.send_message(
            CHAT_ID, f'''A provider has accepted your request! \nProvider details are as follows: 
            \nRequest ID: {data['request']['request_id']}
            \nProvider Name: {data['provider']['first_name'] + " " + data['provider']['last_name']}
            \nProvider ID: {data['provider']['provider_id']}
            \nProvider Location: {data['provider']['location_name']}
            \nProvider Telegram: {data['provider']['tele_id']}
            \n
            \nDetails of your print requests is as follows:
            \nColor: {data['request']['color']}
            \nCopies: {data['request']['no_of_copies']}
            \nSide: {data['request']['single_or_double']}
            \nSize: {data['request']['size']}
            \nComments: {data['request']['comments']}'''
            )
        return jsonify(
            {
                "code": 200,
                "request_id": data['request']['request_id'],
                "provider_id":1
            }), 200

    except Exception as e:
        return jsonify (
            {
                "code": 500,
                "message":"Could not send tele message to requestor.", 
                "error_msg": str(e), 
                "request_id": data['request']['request_id']
            }
        ), 500



#TODO: FOR  PROVIDER: update requestor when their request has been accepted.
#TODO: Change code to take in **data from where ever
@app.route('/update_provider', methods=['POST'])
def update_provider():
    #UNCOMMENT LATER - Data that is passed should be ALL provider, request and requestor details
    data = req.get_json()
    CHAT_ID = data['provider']['chat_id']
    print(CHAT_ID)

    bot.send_message(CHAT_ID, "Testing")
    try:
        bot.send_message(
            CHAT_ID, f"""A provider has accepted your request! \Provider details are as follows: 
            \nRequest ID: {data['request']['request_id']}
            \nRequestor Name: {data['requestor']['first_name'] + " " + data['requestor']['last_name']}
            \nRequestor ID: {data['requestor']['requestor_id']}
            \nRequestor Location: {data['request']['location_name']}
            \nRequestor Telegram: {data['requestor']['tele_id']}
            \n
            \nDetails of your print requests is as follows:
            \nColor: {data['request']['color']}
            \nCopies: {data['request']['no_of_copies']}
            \nSide: {data['request']['single_or_double']}
            \nSize: {data['request']['size']}
            \nComments: {data['request']['comments']}"""
            )

        return jsonify(
            {
                "code": 200,
                "request_id": data['request']['request_id'],
                "provider_id":1
            }), 200

    except Exception as e:
        return jsonify (
            {
                "code": 200,
                "message": "Could not send tele message to provider.", 
                "error_msg": str(e)
            }
        ), 500


if __name__ == "__main__":
    app.run(port=5010, debug=True)



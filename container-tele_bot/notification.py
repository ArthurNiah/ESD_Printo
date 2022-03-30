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
        "chat_id":"263595696", 
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


    try:
        bot.send_message(
            CHAT_ID, f"""A provider has accepted your request! \Provider details are as follows: 
            \nRequest ID: f{data['request']['request_id']}
            \nProvider Name: f{data['provider']['first_name'] + " " + data['provider']['last_name']}
            \nProvider ID: f{data['provider']['provider_id']}
            \nProvider Location: f{data['provider']['location_name']}
            \nProvider Telegram: f{data['provider']['tele_id']}
            \n
            \nDetails of your print requests is as follows:
            \nColor:f{data['request']['color']}
            \nCopies: f{data['request']['no_of_copies']}
            \nSide: f{data['request']['single_or_double']}
            \nSize: f{data['request']['size']}
            \nComments: f{data['request']['comments']}"""
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


    try:
        bot.send_message(
            CHAT_ID, f"""A provider has accepted your request! \Provider details are as follows: 
            \nRequest ID: f{data['request']['request_id']}
            \nRequestor Name: f{data['requestor']['first_name'] + " " + data['requestor']['last_name']}
            \nRequestor ID: f{data['requestor']['requestor_id']}
            \nRequestor Location: f{data['request']['location_name']}
            \nRequestor Telegram: f{data['requestor']['tele_id']}
            \n
            \nDetails of your print requests is as follows:
            \nColor:f{data['request']['color']}
            \nCopies: f{data['request']['no_of_copies']}
            \nSide: f{data['request']['single_or_double']}
            \nSize: f{data['request']['size']}
            \nComments: f{data['request']['comments']}"""
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



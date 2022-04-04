#general imports
import logging
from uuid import uuid4 #new
from requests import api 
from requests.models import encode_multipart_formdata #new
from api import token, chat_id, puja_id


#Import amqp
import amqp_setup
import pika

#Flask imports

from flask import Flask, request as req, jsonify  
from flask_cors import CORS
import os, sys
import requests
import amqp_setup

#Telegram imports
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler, InlineQueryHandler

#Internal files imports
from invokes import invoke_http

monitorBindingKey='.success'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'success'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print("Recording an order log:")
    print(order)


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()


app = Flask(__name__)
CORS(app)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = token
bot = Bot(TOKEN)

#When user first starts their message
#TODO: FOR  REQUESTOR: update requestor when their request has been accepted.
@app.route('/update_requestor', methods=['POST'])
def update_requestor():
    data = req.get_json()
    CHAT_ID = data['requestor']['chat_id'] 

    try:
        bot.send_message(
            CHAT_ID, f'''A provider has accepted your request! \nProvider details are as follows: 
            \nRequest ID: {data['request']['request_id']}
            \nProvider Name: {data['provider']['first_name'] + " " + data['provider']['last_name']}
            \nProvider Location: {data['provider']['location']}
            \nProvider Telegram: {data['provider']['tele_id']}
            \n
            \nDetails of your print requests is as follows:
            \nColor: {data['request']['data']['color']}
            \nCopies: {data['request']['data']['no_of_copies']}
            \nSide: {data['request']['data']['single_or_double']}
            \nSize: {data['request']['data']['size']}
            \nComments: {data['request']['data']['comments']}
            \n\nThe final price of the request will amount to ${data['request']['price']}0. Please ensure that payments are settled with the other party!'''
            )
        return jsonify(
            {
                "code": 200,
                "request_id": data['request']['request_id']
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
@app.route('/update_provider', methods=['POST'])
def update_provider():
    #UNCOMMENT LATER - Data that is passed should be ALL provider, request and requestor details
    data = req.get_json()
    CHAT_ID = data['provider']['chat_id']

    try:
        bot.send_message(
            CHAT_ID, f"""You accepted a request! \nRequestor details are as follows: 
            \nRequest ID: {data['request']['request_id']}
            \nRequestor Name: {data['requestor']['first_name'] + " " + data['requestor']['last_name']}
            \nRequestor ID: {data['request']['data']['requestor_id']}
            \nRequestor Location: {data['request']['data']['location_name']}
            \nRequestor Telegram: {data['requestor']['tele_id']}
            \n
            \nDetails of your print requests is as follows:
            \nColor: {data['request']['data']['color']}
            \nCopies: {data['request']['data']['no_of_copies']}
            \nSide: {data['request']['data']['single_or_double']}
            \nSize: {data['request']['data']['size']}
            \nComments: {data['request']['data']['comments']}
            \n\nDocument to be printed can be found here: {data['request']['document_link']}
            \n\nThe final price of the request will amount to ${data['request']['price']}0.  Please ensure that payments are settled with the other party!"""
            )

        return jsonify(
            {
                "code": 200,
                "request_id": data['request']['request_id']
            }), 200

    except Exception as e:
        return jsonify (
            {
                "code": 500,
                "message": "Could not send tele message to provider.", 
                "error_msg": str(e)
            }
        ), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)



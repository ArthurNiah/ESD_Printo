from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from os import environ

#import internal files
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

import json
import amqp_setup

monitorBindingKey='.success'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'success'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\ SUCCESSFULLY RECEIVED AN ORDER " + __file__)
    # processOrderLog(json.loads(body))
    print(json.loads(body))
    # print() # print a new line feed

# def processOrderLog(order):
#     print("Recording an order log:")
#     print(order)


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
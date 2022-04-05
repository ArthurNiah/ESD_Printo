from flask import Flask, request as req, jsonify
from flask_cors import CORS
import os, sys
# import requests
from os import environ
from flask_sqlalchemy import SQLAlchemy

#import internal files
from invokes import invoke_http
# from request import Request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://is213@host.docker.internal:3306/activity_log'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

import json
import amqp_setup

monitorBindingKey='.success'

class Activity_log(db.Model):
    __tablename__ = 'activity_log'
    log_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, nullable= False)
    # create_datetime = db.Column(db.Integer, nullable= True)


def __init__(self, request_id, log_id = None):
    self.log_id = log_id
    self.request_id = request_id


def json(self):
    return {
        "log_id": self.log_id, 
        "request_id": self.request_id
    }


def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'success'
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\ SUCCESSFULLY RECEIVED AN ORDER " + __file__)
    print("BODY RETURN", body)
    # print(json.loads(body))
    processActivityLog(body)
    # print() # print a new line feed

def processActivityLog(body):
    print("Recording an order log:")


    print("=====START: Insert Log Activity into DB======")
    log = Activity_log("body")

    db.session.add(log)
    db.session.commit()

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()

from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests


# import amqp_setup
import pika
import json

#import internal files
from invokes import invoke_http
# from google_maps import get_current_location

app = Flask(__name__)
CORS(app)




from crypt import methods
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests


# import amqp_setup
import pika
import json

#import internal files
from invokes import invoke_http
from google_maps import get_current_location

app = Flask(__name__)
CORS(app)


request_URL = ""
googleDrive_URL =  ""
googleMaps_URL = "http://localhost:5001/get_current_request"
requestDB_URL = ""


@app.route("/create_request", methods=["POST"])
#For creating a new requestd
def create_request():

    if request.is_json:
        try:
            user_request = request.get_json()
            print("\Created request creation order in JSON:", user_request)

            # do the actual work
            # 1. Send order info {cart items}
            result = processRequest(user_request)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_request.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

#process the data(adpated from the sldies)
def processRequest(user_request):


    #Step 1: Invoking Google Maps microservice
    print('\n-----Invoking GoogleMaps microservice-----')
    locationResults = invoke_http(googleMaps_URL, method="GET", json=user_request) #Replace with variable 
    print("Current requestor location:", locationResults)


    #Step 2: Invoking Request microservice (Update to be done in the Req Microservice)
    print('\n-----Invoking Request microservice-----')
    invoke_http(request_URL, method="POST", json=user_request)



    #Step 3: Updating Google Drive microservice IF update request works
    print('\n-----Invoking GoogleDrive microservice-----')
    invoke_http(googleDrive_URL, method='POST', json=user_request)



    return "Placeholder"



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(port=5000, debug=True)
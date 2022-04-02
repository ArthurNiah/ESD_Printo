
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


insert_provider_URL = "http://localhost:5007/provider" #take note which localhost number you using and calling
googleMaps_URL = "http://localhost:5002/get_current_location" #take note which localhost number you using and calling

#Info from UI
user_input = {}


@app.route("/create_provider", methods=["POST"])
#For creating a new request
def create_provider():

    if request.is_json:
        try:
            provider_details = request.get_json()
            print("\Created provider details in JSON:", provider_details)

            # do the actual work
            # 1. Send order info {cart items}
            result = processProvider(provider_details)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_provider.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

#process the data(adpated from the sldies)
def processProvider(provider_details):

    #Step 1: Invoking Google Maps microservice
    print('\n-----Invoking GoogleMaps microservice-----')
    locationResults = invoke_http(googleMaps_URL, method="GET", json=provider_details) #Replace with variable 

    #====START: Error handeling for Google Maps API======
    if locationResults['code'] not in range(200, 300):

        # Inform the error microservice
        print('\n\n-----Google Maps API microservice has failed-----')

        #Return error to UI???
        return {
            "code": 500,
            "message": "Google Maps Microservice API has failed. Please read error message and try again.",
            "errorMsg": locationResults['message']
        }
    #====END: Error handeling for Google Maps API======

    #update to provider_details
    provider_details['lat'] = locationResults['data']['lat']
    provider_details['lng'] = locationResults['data']['lng']
    provider_details['place_id'] = locationResults['data']['placeID']
    provider_details['location_name'] = locationResults['data']['locationName']

    #Step 2: Invoking Provider microservice (Update to be done in the Provider Microservice)
    print('\n-----Invoking Provider microservice-----')
    provider_results = invoke_http(insert_provider_URL, method="POST", json=provider_details)

    #====START: Error handeling for Provider Microservice======
    #Error for creating provider
    if provider_results['code'] == 500:

        #Return error to UI???
        return {
            "code": 500,
            "message": "An error occurred in creating the Provider.",
        }

    #====END: Error handeling for Provider Microservice======


    return{
        "code": 201,
        "data": {
            "message": "Provider details was added successfully!"
        }
    }


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an request...")
    app.run(port=5006, debug=True)
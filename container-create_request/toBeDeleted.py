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
# from google_maps import get_current_location

app = Flask(__name__)
CORS(app)


request_URL = "http://localhost:5003/insert_request"
update_location_URL = "http://localhost:5003/update_location_name/"
googleDrive_URL = "http://localhost:3000/insert_document"
googleMaps_URL = "http://localhost:5002/get_current_location"
requestDB_URL = ""

#Info from UI
user_input = {
    
}


@app.route("/create_request", methods=["POST"])
#For creating a new requestd
def create_request():

    if request.is_json:
        try:
            user_request = request.get_json()
            print("\Created request creation order in JSON:", user_request)

            # do the actual work
            # 1. Send order info {cart items}
            result = processRequest(user_request = {"requestor_id": 619, "location":"SMU" })
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



    #Step 2: Invoking Request microservice (Update to be done in the Req Microservice)
    print('\n-----Invoking Request microservice-----')
    # Need to find a way to add new data into a json file
    request_results = invoke_http(request_URL, method="POST", json=user_request)
    invoke_http(update_location_URL+str(request_results['data']['request_id']), method="POST", json=locationResults['data'])
    #====START: Error handeling for Request Microservice ======
    if request_results['code'] not in range(200, 300):

        # Inform the error microservice
        print('\n\n-----Request microservice has failed-----')

        #Return error to UI???
        return {
            "code": 500,
            "message": "Request Microservice API has failed. Please read error message and try again.",
            "errorMsg": request_results['message']
        }



    
    #====END: Error handeling for Request Microservice ======


    # #Step 3: Updating Google Drive microservice IF update request works
    # print('\n-----Invoking GoogleDrive microservice-----')
    # drive_result = invoke_http(googleDrive_URL, method='POST', json=user_request)

    # #====START: Error handeling for Google Drive API Microservice ======
    # if drive_result['code'] not in range(200, 300):

    #     print('\n\n-----Google Drive microservice has failed-----')

    #     #Return error to UI???
    #     return {
    #         "code": 500,
    #         "message": "Google Drive Microservice API has failed. Please read error message and try again.",
    #         "errorMsg": drive_result['message']
    #     }
    # #====END: Error handeling for Google Drive API Microservice ======



    return{
        "code": 201,
        "data": {
            "message": "Print request was added successfully! Cross your fingers and lets hope for the best!"
        }
    }




if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an request...")
    app.run(port=5001, debug=True)
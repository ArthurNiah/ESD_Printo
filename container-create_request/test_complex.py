
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests


# import amqp_setup
import pika
import json

#import internal files
from invokes import invoke_http

app = Flask(__name__)
CORS(app)


request_URL = "http://localhost:5002/insert_request"
googleDrive_URL = "http://localhost:3000/insert_document"
googleMaps_URL = "http://localhost:5001/get_current_request"
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
            print('user_request', user_request)
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

    #Step 3: Updating Google Drive microservice IF update request works
    print('\n-----Invoking GoogleDrive microservice-----')
    print("request", user_request)
    #response = invoke_http(googleDrive_URL, method='POST', json=user_request)
    #print('response', response)
    response = requests.post(googleDrive_URL, data=user_request)
    print("response: ", response.text)
    #====START: Error handeling for Google Drive API Microservice ======
    if response.status_code != 200:

        print('\n\n-----Google Drive microservice has failed-----')
        #Return error to UI???
        return {
            "code": 500 ,
            "message": "Google Drive Microservice API has failed. Please read error message and try again.",
            "errorMsg": "Error"
        }
    #====END: Error handeling for Google Drive API Microservice ======



    return{
        "code": 201,
        "data": {
            "message": "Print request was added successfully! Cross your fingers and lets hope for the best!"
        }
    }




if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an request...")
    app.run(port=5005, debug=True)
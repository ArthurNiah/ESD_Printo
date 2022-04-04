
from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from os import environ

#import internal files
from invokes import invoke_http

app = Flask(__name__)
CORS(app)


request_URL = environ.get('request_URL') 
update_location_URL = environ.get('update_location_URL') 
update_gdrive_URL = environ.get('update_gdrive_URL') 
googleDrive_URL = environ.get('googleDrive_URL') 
googleMaps_URL = environ.get('googleMaps_URL') 
print_details_URL = environ.get('print_details_URL') 

#Info from UI
user_input = {
}


@app.route("/create_request", methods=["POST"])
#For creating a new requestd
def create_request():
    user_request = request.get_json()
    print(user_request)
    if request.is_json:
        try:
            user_request = request.get_json()
            # user_request = {"requestor_id": 123, "location":"SMU", "file_name": "popcat.gif" }
            print("\Created request creation order in JSON:", user_request)

            # do the actual work
            # 1. Send order info {cart items}
            # result = processRequest(user_request = {"requestor_id": 123, "location":"SMU", "file_name": "popcat.gif" }
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
    print("Current requestor location:", locationResults['data'])

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
    print('\n-----GoogleMaps microservice SUCCESS-----')


    #Step 2: Invoking Request microservice (Update to be done in the Req Microservice)
    print('\n-----Invoking Request microservice-----')
    # Need to find a way to add new data into a json file
    request_results = invoke_http(request_URL, method="POST", json=user_request)
    invoke_http(update_location_URL+str(request_results['data']['request_id']), method="PUT", json=locationResults['data'])
    test = invoke_http(print_details_URL+str(request_results['data']['request_id']), method="PUT", json=user_request)
    print("\n\n HELLOE CHECKKCKCKCK", user_request)
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
    print('\n-----Request microservice SUCCESS-----')



    
    #====END: Error handeling for Request Microservice ======

    #Step 3: Updating Google Drive microservice IF update request works
    print('\n-----Invoking GoogleDrive microservice-----')
    print("request", user_request)
    #response = invoke_http(googleDrive_URL, method='POST', json=user_request)
    #print('response', response)
    response = requests.post(googleDrive_URL, data=user_request)
    # print(response.text)
    #====START: Error handeling for Google Drive API Microservice ======
    if response.status_code != 200:

        print('\n\n-----Google Drive microservice has failed-----')
        #Return error to UI???
        return {
            "code": 500 ,
            "message": "Google Drive Microservice API has failed. Please read error message and try again.",
            "errorMsg": "Error"
        }

    #ADDING GDRIVE LINK TO DB
    isSuccess = invoke_http(update_gdrive_URL+str(request_results['data']['request_id']), method="PUT", json=response.text)
    print("HELLO ATTENTION HERE", isSuccess)
    #====END: Error handeling for Google Drive API Microservice ======
    print('\n-----GDrive microservice SUCCESS-----')



    return{
        "code": 201,
        "data": {
            "message": "Print request was added successfully! Cross your fingers and lets hope for the best!"
        }
    }



if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an request...")
    app.run(host='0.0.0.0',port=5001, debug=True)
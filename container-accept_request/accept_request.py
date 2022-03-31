from crypt import methods
from multiprocessing.spawn import get_preparation_data
from flask import Flask, request as req, jsonify
from flask_cors import CORS
import os, sys
from pkg_resources import get_provider
import requests


# import amqp_setup
import pika
import json

#import internal files
from invokes import invoke_http
# from google_maps import get_current_location

app = Flask(__name__)
CORS(app)


#INPUT
# {
# request_id: 1, 
# provider_id: 2}

get_request_URL = "http://localhost:5003/search_request/"
update_provider_id_URL = "http://localhost:5003/update_provider_id/"
update_status_URL = "http://localhost:5003/update_status/"
get_provider_URL = "http://localhost:5007/provider/"
get_requestor_URL = "http://localhost:5005/requestor/"
notification_update_requestor_URL = "http://localhost:5010/update_requestor"
notification_update_provider_URL = "http://localhost:5010/update_provider"



@app.route("/accept_request/<string:request_id>", methods=['POST'])
def accept_request(request_id):

    data = req.get_json()

    #STEP 1: Get Provider Info
    print('\n-----Invoking Provider microservice-----')
    get_provider_res = invoke_http(get_provider_URL + str(data['provider_id']), json = data)
    print(get_provider_res)
    if get_provider_res['code'] not in range(200,300):
        
        print("\n-----FAILED: Invoking Provider microservice-----")

        return jsonify(
            {
                "code": 500, 
                "message": "Failed to invoke provider microservice."
            }
        )

    #STEP 2: Get request Info
    get_request_res = invoke_http(get_request_URL + str(request_id), json = data)
    print('\n-----Invoking Request microservice-----')
    print(get_request_res)
    if get_request_res['code'] not in range(200,300):
        
        print("\n-----FAILED: Invoking Request microservice-----")

        return jsonify(
            {
                "code": 500, 
                "message": "Failed to invoke request microservice."
            }
        )

    #STEP 3: Update request with provider_id + status + print_details
    #TODO: Update request with print details
    print('\n-----Invoking Update Request microservice-----')
    update_provider_id_res= invoke_http(update_provider_id_URL + str(data['request_id']), json = data, method='PUT')
    update_status= invoke_http(update_status_URL + str(data['request_id']), json = {"status":"Accepted"}, method='PUT')
    print(update_provider_id_res)
    if update_provider_id_res['code'] not in range(200,300):
        
        print("\n-----FAILED: Invoking Update Provider microservice-----")

        return jsonify(
            {
                "code": 500, 
                "message": "Failed to update provider microservice."
            }
        )

    #STEP 4: Get Requestor Info
    print('\n-----Invoking Requestor microservice-----')
    get_requestor_res= invoke_http(get_requestor_URL + str(get_request_res['data']['response']['requestor_id']), json = data, method='GET')
    print(get_requestor_URL + str(get_request_res['data']['response']['requestor_id']))
    print(get_requestor_res)
    if get_requestor_res['code'] not in range(200,300):
        
        print("\n-----FAILED: Invoking Requestor microservice-----")

        return jsonify(
            {
                "code": 500, 
                "message": "Failed to invoke requestor microservice."
            }
        )

    #STEP 5: Collate info and invoke Notification.py
    print("\n-----Invoking Telegram Notification microservice-----")
    collated_info = {
        "request": {
            "request_id": get_request_res['data']['request_id'], 
            "data": get_request_res['data']['response']
        },
        "provider": get_provider_res['data'],
        "requestor": get_requestor_res['data']
    }

    notify_requestor_res = invoke_http(notification_update_requestor_URL, json = collated_info, method = 'POST')
    notify_provider_res = invoke_http(notification_update_provider_URL, json=collated_info, method = 'POST')
    print(notify_provider_res)
    print(notify_requestor_res['code'])
    if notify_provider_res['code'] not in range(200,300) or notify_requestor_res['code'] not in range(200, 300):
        print("\n-----FAILED: Invoking Telegram Notification microservice-----")
        return jsonify (
            {
                "code":500, 
                "message" :{
                    "requestor_side": "hello", 
                    "provider_side": "hello"
                }
            }
        )
    #return success of failure code

    return jsonify(
        {
            "code": 200, 
            "message": "Succesfully accepted request. Please refer to the detail sent on Telegram."
        }
    )

if __name__ == "__main__":
    app.run(port=5009, debug=True)
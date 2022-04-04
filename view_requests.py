# FILTER_REQUESTS COMPLEX MICROSERVICE
from operator import index
from flask import Flask, request as req, jsonify

# to read requests/retrieve data from other APIs
import requests
from invokes import invoke_http

# for database
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# for containerization later on
from os import environ

# api key (Sabbie's)
api_key = 'AIzaSyAtQumxZP0XtDgLgYSV8Fcb8heVm5VRlJE'
# ---------------------------------------------------------------------------------------------------------------- #
app = Flask(__name__)
CORS(app)

# URLs for invoke_http
get_all_request_locations_url = environ.get('get_all_request_locations_url')
get_provider_location_url = environ.get('get_provider_location_url')


@app.route("/filter_requests", methods=['GET'])
def filter_requests():

    data = req.get_json()
    
    # 1. Get location_name, request_id, place_id of all requests in database
    print('\n-----Invoking Request microservice-----')
    resp = invoke_http(get_all_request_locations_url, method="GET")
    print(resp)

    # Error Handling
    if resp['code'] not in range(200,300):
        
        print("\n-----FAILED: Invoking Request microservice-----")

        return jsonify(
            {
                "code": 500, 
                "message": "Failed to invoke request microservice."
            }
        )


    # 2. Store in obtained details in list
    all_req = []
    for i in range(len(resp["data"]["request"])):
        single_request = { 
            "request_id": resp["data"]["request"][i]["request_id"], 
            "location_name": resp["data"]["request"][i]["location_name"], 
            "place_id": resp["data"]["request"][i]["place_id"]
            }
        all_req.append(single_request)


    # 3. Format string for API and list for comparison later on
    request_place_id_str = ""
    for i in range(len(all_req)):
        request_place_id_str += "place_id:"+all_req[i]["place_id"]+"|"
    request_locations = request_place_id_str


    print('\n-----Invoking Provider microservice-----')
    provider_results = invoke_http(get_provider_location_url+str(data['provider_id']), method="GET")
    print(provider_results)

    # Error Handling
    if provider_results['code'] not in range(200,300):
            
            print("\n-----FAILED: Invoking Provider microservice-----")

            return jsonify(
                {
                    "code": 500, 
                    "message": "Failed to invoke provider microservice."
                }
            )    

    provider_place_id = provider_results["data"]["place_id"]
    provider_location = "place_id:"+provider_place_id+"|"

    # ------------------------------------------------------------------------------ #
    origin = provider_location
    destinations = request_locations

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destinations}&mode=walking&key={api_key}"
    
    output_json = requests.get(url).json()

    #return output_json

    try:
        # if there are no requests in the database
        if len(output_json) == 0:
            return jsonify(
                {
                    "code": 404, 
                    "message": "There are no requests. Please try again later!"
                }, 
            ), 404            

        else:
            # dict of all places >500m away (walking)
            index_list = []
            nearby_requests = {} 

            # list of distance and travel duration for all requests
            dist_dur_elements = output_json["rows"][0]["elements"]
            
            # reiterate through list to get distance and index of locations that are nearby
            for i in range(len(dist_dur_elements)):
                if dist_dur_elements[i]["distance"]["value"] < 501:
                    index_list.append(i)
                    
            # if there are no nearby requests
            if len(index_list) == 0:
                return jsonify(
                    {
                        "code": 404, 
                        "message": "There are no requests near you."
                    }, 
                ), 404

            for i in range(len(index_list)):
                if i == 5:
                    break
                nearby_requests[i+1] = all_req[index_list[i]]

            return nearby_requests
            #return output_json

    except Exception as e:
        return jsonify(
            {
                'code': 500, 
                "message": "An error occurred while fetching requests:" + str(e)
            },
        ), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5008, debug=True)
# SCENARIO 3 STEP 6: FILTER REQUEST LOCATIONS BASED ON DISTANCE
from flask import Flask, request, jsonify

# to read requests/retrieve data from other APIs
import requests
from invokes import invoke_http
from get_provider_location import get_provider_location

# for database
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# for containerization later on
from os import environ


# api key (Sabbie's)
api_key = 'AIzaSyAtQumxZP0XtDgLgYSV8Fcb8heVm5VRlJE'
# ---------------------------------------------------------------------------------------------------------------- #
app = Flask(__name__)



get_request_locations_url = "http://localhost:5001/get_request_locations"
request_locations = invoke_http(get_request_locations_url, method="GET")
all_requests = request_locations["data"] # {req_id: place_id}
# populate requestLocations w/ results of get_request_locations fn
# sample data (smu, marine drive, marine drive [repeated])
# requestLocations = "place_id:ChIJGddBg6MZ2jERACsxW7Ovm_4|place_id:ChIJAfIKr3YY2jERy7LqQJFre-A|place_id:ChIJAfIKr3YY2jERy7LqQJFre-A|"


get_provider_location_url = "http://localhost:5000/get_provider_location/2"
provider_results = invoke_http(get_provider_location_url, method="GET")
provider_location = provider_results["place_id"]
# provider_location = "place_id:ChIJiSjdY3QY2jERl_jWgSll1_o"
# providerLocation = "278 Marine Parade Rd, #01-02 Community Building, Singapore 449282"

# populate providerLocation w/ provider placeID
# providerLocation = "NUS"


# need to check error handling
@app.route("/filter_requests", methods=['GET'])
def filter_requests(pLoc=provider_location, req_dict=all_requests):
    """
    Return all requests that are <=500m away from the provider.

    Input needed:
    1. Provider Location (Address)
    2. All Request Locations (Address)

    Use distance matrix API: get walking distance

    Return: the distances between the provider's location (Origin) and request locations (Destination)
    
    all_requests = {req_id: place_id}

    1. format the destinations string
    - obtain keys and concatenate

    2. put place_id into a list --> index

    3. based on index of place in "elements" list: distance key, value key, match with index of place_id in list

    4. cut off list at 5 and return
    
    """
    origin = provider_location
    destinations = all_requests
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destinations}&mode=walking&key={api_key}"
    
    # to read in browser/postman
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
            nearby_requests = {}

            # list of distance and travel duration for all requests
            dist_dur_list = output_json["rows"][0]["elements"]
            
            # reiterate through list to get distance and index of locations that are nearby
            for i in range(len(dist_dur_list)):
                if dist_dur_list[i]["distance"]["value"] < 501:
                    nearby_requests[output_json["destination_addresses"][i]] = dist_dur_list[i]["distance"]["value"]
                    
            if len(nearby_requests) == 0:
                return jsonify(
                    {
                        "code": 404, 
                        "message": "There are no requests near you."
                    }, 
                ), 404    
            # error handling: when 2 requests have the same location --> store values in list?
            # request id as key, location and distance as value (tuple)
            # hOWwwwwwwwwWW


            # can only return dict, tuples
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
    app.run(port=5003, debug=True)

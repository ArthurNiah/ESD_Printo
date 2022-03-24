import requests

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # to input objects into the database
from os import environ

# api key (Sabbie's)
api_key = 'AIzaSyAtQumxZP0XtDgLgYSV8Fcb8heVm5VRlJE'

app = Flask(__name__)

# populate requestLocations w/ results of locate_all_requests fn / locations in db
# sample data (smu, marine drive, marine drive [repeated])
requestLocations = "place_id:ChIJGddBg6MZ2jERACsxW7Ovm_4|place_id:ChIJAfIKr3YY2jERy7LqQJFre-A|place_id:ChIJAfIKr3YY2jERy7LqQJFre-A"

# populate providerLocation w/ provider placeID
# sample data (marine parade library)
providerLocation = "place_id:ChIJiSjdY3QY2jERl_jWgSll1_o"


# need to implement error handling!! --> if no requests in the db and no requests nearby
@app.route("/filter_requests", methods=['GET'])
def filter_requests(pLoc=providerLocation, rLoc=requestLocations):
    """
    Return all requests that are <=500m away from the provider.

    Input needed:
    1. Provider Location (Address)
    2. All Request Locations (Address)

    Use distance matrix API: get walking distance

    Return: the distances between the provider's location (Origin) and request locations (Destination)
    """

    origin = providerLocation
    destinations = requestLocations
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destinations}&mode=walking&key={api_key}"
    
    # to read in browser/postman
    output_json = requests.get(url).json()

    try:

        # if there are no requests in the database
        if len(output_json) == 0:
            return jsonify(
                {
                    "code": 404, 
                    "message": "Location was not valid. Please try again!"
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
                    

            # error handling: when 2 requests have the same location --> store values in list?
            # maybe request id as key, location and distance as value (tuple)
            # hOWwwwwwwwwWW


            # can only return dict, tuples
            return nearby_requests
            # return output_json

    except Exception as e:
        return jsonify(
            {
                'code': 500, 
                "message": "An error occurred while fetching your location;" + str(e)
            },
        ), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)

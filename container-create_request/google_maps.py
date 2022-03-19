import googlemaps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import requests
from invokes import invoke_http

app = Flask(__name__)

API_KEY = 'AIzaSyA2wZe6-CgWyeoEJha5aeZLQp-cpn4kb8k'

# #WORKS
@app.route("/get_current_location", methods=['GET'])
def get_current_location(user_location="NUS"):

    try:

        map_client = googlemaps.Client(API_KEY)
        response = map_client.geocode(user_location)

        if response == []:
            return jsonify(
                {
                    "code": 404, 
                    "data": user_location,
                    "message": "Location was not valid. Please try again!"
                }, 
            ), 404

        #return the location
        else:
            #Getting a placeID to be used for storage
            place_id = response[0]['place_id']
            print(place_id)
            #Reverse Geocoding, Takes the place id and returns a location
            url2 = f"https://maps.googleapis.com/maps/api/geocode/json?place_id={place_id}&key={API_KEY}"
            rev_geoencode = invoke_http(url2, method="GET")
            formatted_address = rev_geoencode['results'][0]['formatted_address']
            user_lat = response[0]['geometry']['location']['lat']
            user_lng = response[0]['geometry']['location']['lng']
            return jsonify(
                {
                    "code": 201, 
                    "data": {
                        "user_input": user_location,
                        "placeID" : place_id, 
                        "locationName" : formatted_address,
                        "lat": user_lat, 
                        "lng": user_lng
                    },
                }
            ), 201

        

    except Exception as e:
        return jsonify(
            {
                'code': 500, 
                "data": user_location,
                "message": "An error occurred while fetching your location. " + str(e)
            },
        ), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)



#FOR DEBUGGING PURPOSES (REMOVE AT THE END OF PROJECT!!!)
# map_client = googlemaps.Client(API_KEY)
# response = map_client.geocode("NUS")
# print(response[0]['geometry']['location']['lat'])
# print(response[0]['geometry']['location']['lng'])

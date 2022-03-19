import googlemaps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

API_KEY = 'AIzaSyA2wZe6-CgWyeoEJha5aeZLQp-cpn4kb8k'

# user_lat, user_long = map_client.geolocate()['location']['lat'], map_client.geolocate()['location']['lng']
# url1 =f"https://maps.googleapis.com/maps/api/geocode/json?latlng={user_lat},{user_long}&key={API_KEY}"

# # user_location = invoke_http(url, method="GET")
# user_location = requests.request('GET', url2)
# print(user_location.json()['results'][0]['formatted_address'])
# print(url)
# print(user_location['results'])


#WORKS
@app.route("/get_current_location", methods=['POST'])
def get_current_location(user_location):

    try:

        map_client = googlemaps.Client(API_KEY)
        temp_place_id = map_client.geocode(user_location)[0]['place_id']

        #Reverse Geocoding, Takes the place id and returns a location
        url2 = f"https://maps.googleapis.com/maps/api/geocode/json?place_id={temp_place_id}&key={API_KEY}"
        response = invoke_http(url2, method="GET")

        if not response:
            return jsonify(
                {
                    "code": 404, 
                    "data": user_location,
                    "message": "Location was not found. Please try again!"
                }, 
            ), 404

        #return the location
        else:
            return jsonify(
                {
                    "code": 201, 
                    "data": response['results'][0]['formatted_address'],
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

# map_client = googlemaps.Client(API_KEY)
# temp_place_id = map_client.geocode('NUS')[0]['place_id']

# #Reverse Geocoding, Takes the place id and returns a location
# url2 = f"https://maps.googleapis.com/maps/api/geocode/json?place_id={temp_place_id}&key={API_KEY}"
# response = invoke_http(url2, method="GET")
# print(response['results'][0]['formatted_address'])
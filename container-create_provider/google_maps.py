import googlemaps
from flask import Flask, request as req, jsonify
from invokes import invoke_http

app = Flask(__name__)

API_KEY = 'AIzaSyA2wZe6-CgWyeoEJha5aeZLQp-cpn4kb8k'

# #WORKS
@app.route("/get_current_location", methods=['GET'])
def get_current_location():

    map_client = googlemaps.Client(API_KEY)
    data = req.get_json()
    response = map_client.geocode(data['location'])
    try:

        if response == []:
            return jsonify(
                {
                    "code": 404, 
                    "data": data['location'],
                    "message": "Location was not valid. Please try again!"
                }, 
            ), 404

        #return the location
        else:
            #Getting a placeID to be used for storage
            place_id = response[0]['place_id']
            #Reverse Geocoding, Takes the place id and returns a location
            url2 = f"https://maps.googleapis.com/maps/api/geocode/json?place_id={place_id}&key={API_KEY}"
            rev_geoencode = invoke_http(url2, method="GET")
            formatted_address = rev_geoencode['results'][0]['formatted_address']
            user_lat = response[0]['geometry']['location']['lat']
            user_lng = response[0]['geometry']['location']['lng']
            return jsonify(
                {
                    "code": 200, 
                    "data": {
                        "user_input": data['location'],
                        "place_id" : place_id, 
                        "location_name" : formatted_address,
                        "coordinates": str(user_lat) + " " + str(user_lng) 
                    },
                }
            ), 200


    except Exception as e:
        return jsonify(
            {
                'code': 500, 
                "message": "An error occurred while fetching your location. " + str(e)
            },
        ), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)



#FOR DEBUGGING PURPOSES (REMOVE AT THE END OF PROJECT!!!)
# map_client = googlemaps.Client(API_KEY)
# response = map_client.geocode("NUS")
# print(response[0]['geometry']['location']['lat'])
# print(response[0]['geometry']['location']['lng'])

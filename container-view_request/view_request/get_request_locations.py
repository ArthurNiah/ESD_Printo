# SCENARIO 3 STEP 6: retrieving all the request locations
from flask import Flask, request, jsonify

# for database
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# for containerization later on
from os import environ

# to retrieve requests 
import requests

# ---------------------------------------------------------------------------------------------------------------- #

app = Flask(__name__)

# connect to provider database remotely (need to set dbURL)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

# type into cmd prompt
# set dbURL=mysql+mysqlconnector://root@localhost:3306/request
# dbURL=mysql+mysqlconnector://<USER_WITH_REMOTE_ACCESS>@host.docker.internal:3306/request

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/request'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Request(db.Model):
    __tablename__ = 'request'

    # basic info
    request_id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, nullable= False)
    provider_id = db.Column(db.Integer, nullable= True)
    status = db.Column(db.String(32), nullable=True)
    document_id = db.Column(db.String(100), nullable=True)
    # create_datetime= db.Column(db.Timestamp, nullable= False)

    # gmaps info
    coordinates = db.Column(db.String(100), nullable=True)
    location_name = db.Column(db.String(100), nullable=True)
    place_id = db.Column(db.String(100), nullable=True)

    # for printing info
    color = db.Column(db.String(32), nullable=True)
    no_of_copies = db.Column(db.Integer, nullable=True)
    single_or_double = db.Column(db.String(32), nullable=True)
    size = db.Column(db.String(10), nullable=True)
    comments = db.Column(db.String(100), nullable=True)


    # def __init__(self, requestor_id, provider_id, status, document_link, coordinates, location_name):
# TODO: Try changing the database to Null values upon init
    def __init__(self, 
    requestor_id, 
    status='Unaccepted', 
    provider_id= None, 
    document_id = None, 
    coordinates = None, 
    location_name=None, 
    color = None, 
    no_of_copies = 0, 
    single_or_double = None, 
    size = None, 
    comments = None,
    ):
        self.requestor_id= requestor_id   
        self.provider_id= provider_id
        self.status= status
        self.document_id= document_id
        self.coordinates= coordinates
        self.location_name = location_name
        self.color = color
        self.no_of_copies = no_of_copies
        self.single_or_double = single_or_double
        self.size = size
        self.comments = comments

    def json(self):
        return {
        "requestor_id": self.requestor_id, 
        "provider_id": self.provider_id, 
        "status": self.status,
        "document_id": self.document_id,
        "location_name": self.location_name, 
        "coordinates" : self.coordinates,
        "color": self.color, 
        "no_of_copies": self.no_of_copies, 
        "single_or_double": self.single_or_double, 
        "size": self.size,
        "comments":self.comments
        }

# Obtain all requests locations (location name, place id + request id?)
@app.route("/get_request_locations")
def get_request_locations():

    requestlist = Request.query.all()
    if len(requestlist):
        
        # need to test
        # dictionary of success code + request_id (key) and place_id (value)
        all_locations = {
            "code": 200,
            "data": {},
            "place_ids": ""
        }

        for destination in requestlist:
            all_locations["data"][destination.request_id] = destination.place_id

        for (key, value) in all_locations["data"].items():
            all_locations["place_ids"] += "place_id:"+value+"|"
        

        return jsonify(all_locations)
        # return request.get_json()

    return jsonify(
        {
            "code": 404,
            "message": "There are no requests available."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
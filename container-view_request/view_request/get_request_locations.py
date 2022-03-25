# SCENARIO 3 STEP 6: retrieving all the request locations
from flask import Flask, request, jsonify

# for database
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# for containerization later on
from os import environ

# to retrieve requests 
import requests

# api key (Sabbie's)
api_key = 'AIzaSyAtQumxZP0XtDgLgYSV8Fcb8heVm5VRlJE'

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

# NEED TO CHECK TABLE STRUCTURE AGAIN AND TEST
class Request(db.Model):
    __tablename__ = 'request'

    request_id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, nullable=False)
    provider_id = db.Column(db.Integer, nullable=False)
    document_link = db.Column(db.String(64), nullable=False)
    coordinates = db.Column(db.String(64), nullable=False)
    location_name = db.Column(db.String(64), nullable=False)
    place_id = db.Column(db.String(64), nullable = False) # added place_id first
    create_datetime = db.Column(db.datetime, nullable=False, default=db.datetime.datetime.utcnow)
    status = db.Column(db.String(64), nullable=False, default="UNACCEPTED")

    """
    need to check again:
        1. `status` varchar(32) NOT NULL DEFAULT 'UNACCEPTED'

        2. `create_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    """

    def __init__(self, request_id, requestor_id, provider_id, document_link, coordinates, location_name, place_id, create_datetime, status):
        self.request_id = request_id
        self.requestor_id = requestor_id
        self.provider_id = provider_id
        self.document_link = document_link
        self.coordinates = coordinates
        self.location_name = location_name
        self.place_id = place_id # added place_id first
        self.create_datetime = create_datetime
        self.status = status

    def json(self):
        return {"request_id": self.request_id, "requestor_id": self.requestor_id, "provider_id": self.provider_id, "document_link": self.document_link, "coordinates": self.coordinates, "location_name": self.location_name, "place_id": self.place_id, "create_datetime": self.create_datetime, "status": self.status}


# Obtain all requests locations (location name, place id + request id?)
@app.route("/get_request_locations")
def get_request_locations():

    requestlist = Request.query.all()
    if len(requestlist):
        
        # dictionary of success code + location names (key) and placeIDs (value)
        location_placeIDs = {
            "code": 200,
            "data": {}
        }

        for destination in requestlist:
            location_placeIDs["data"][destination.locationName] = destination.placeID
        

        return jsonify(location_placeIDs)

    return jsonify(
        {
            "code": 404,
            "message": "There are no requests available."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy # to input objects into the database
from os import environ

# api key (Sabbie's)
api_key = 'AIzaSyAtQumxZP0XtDgLgYSV8Fcb8heVm5VRlJE'


app = Flask(__name__)

# connect to requestor database (need to set dbURL)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# set dbURL=mysql+mysqlconnector://root@localhost:3306/REQUESTOR-DB-NAME (no remote access) (cmd prompt)
# dbURL=mysql+mysqlconnector://USER_WITH_REMOTE_ACCESS@host.docker.internal:3306/REQUESTOR-DB-NAME (cmd prompt)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


# CHANGE TO REQUESTS TABLE STRUCTURE LATER
class Request(db.Model):
    __tablename__ = 'requests'

    isbn13 = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)

    def __init__(self, isbn13, title, price, availability):
        self.isbn13 = isbn13
        self.title = title
        self.price = price
        self.availability = availability

    def json(self):
        return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}


# Obtain all requests locations (location name, place id + request id?)(refer to book_copy.py)
@app.route("/locate_all_requests")
def locate_all_requests():

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
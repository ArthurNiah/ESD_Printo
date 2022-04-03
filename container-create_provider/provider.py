from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
CORS(app)
 
class Provider(db.Model):
    __tablename__ = 'provider'
 
    provider_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    tele_id = db.Column(db.String(64), nullable=False)
    coordinates = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    place_id = db.Column(db.String(64), nullable=False)
    chat_id = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
 
    def __init__(self, username, tele_id, coordinates, location, place_id, chat_id, first_name, last_name):
        self.username = username
        self.tele_id = tele_id
        self.coordinates = coordinates
        self.location = location
        self.place_id = place_id
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name

 
    def json(self):
        return {
        "username": self.username, 
        "tele_id": self.tele_id,
        "coordinates": self.coordinates,
        "location": self.location,
        "place_id": self.place_id,
        "chat_id": self.chat_id,
        "first_name": self.first_name,
        "last_name": self.last_name
        }
 
@app.route("/provider")
def get_all():
    providerlist = Provider.query.all()
    if len(providerlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "providers": [provider.json() for provider in providerlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no providers."
        }
    ), 404
 
@app.route("/provider/<string:provider_id>")
def find_by_provider_id(provider_id):
    provider = Provider.query.filter_by(provider_id=provider_id).first()
    if provider:
        return jsonify(
            {
                "code": 200,
                "data": provider.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Provider not found."
        }
    ), 404

@app.route("/find_by_provider_username/<string:provider_username>")
def find_by_provider_username(provider_username):
    provider = Provider.query.filter_by(provider_username=provider_username).first()
    if provider:
        return jsonify(
            {
                "code": 200,
                "data": provider.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Provider not found."
        }
    ), 404


@app.route("/provider", methods=['POST'])
def insert_provider():

    data = request.get_json()
    provider = Provider(**data)

    # username = request.json.get('username', None)
    # tele_id = request.json.get('tele_id', None)
    # coordinates = request.json.get('coordinates', None)
    # location_name = request.json.get('location_name', None)

    # provider = Provider(username=username, tele_id=tele_id, coordinates=coordinates, location_name=location_name)
 
    try:
        db.session.add(provider)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the Provider."
            }
        ), 500
 
    return jsonify(
        {
            "code": 201,
            "provider_id" : provider.provider_id,
            "data": provider.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)  
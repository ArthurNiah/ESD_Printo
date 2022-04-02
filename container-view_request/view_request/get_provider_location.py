# SCENARIO 3 STEP 4/5: get provider location
from flask import Flask, request, jsonify

# for database
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# for containerization later on
from os import environ

# ---------------------------------------------------------------------------------------------------------------- #
app = Flask(__name__)

# connect to provider database remotely (need to set dbURL)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')

# in cmd prompt
# set dbURL=mysql+mysqlconnector://root@localhost:3306/provider (no remote access) (cmd prompt)
# dbURL=mysql+mysqlconnector://<USER_WITH_REMOTE_ACCESS>@host.docker.internal:3306/provider (cmd prompt)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/provider'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Provider(db.Model):
    __tablename__ = 'provider'
 
    provider_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    tele_id = db.Column(db.String(64), nullable=False)
    lat = db.Column(db.String(64), nullable=False)
    lng = db.Column(db.String(64), nullable=False)
    location_name = db.Column(db.String(64), nullable=False)
    place_id = db.Column(db.String(64), nullable=False)
    chat_id = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
 
    def __init__(self, username, tele_id, lat, lng, location_name, place_id, chat_id, first_name, last_name):
        self.username = username
        self.tele_id = tele_id
        self.lat = lat
        self.lng = lng
        self.location_name = location_name
        self.place_id = place_id
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name

 
    def json(self):
        return {
        "username": self.username, 
        "tele_id": self.tele_id,
        "lat": self.lat,
        "lng": self.lng,
        "location_name": self.location_name,
        "place_id": self.place_id,
        "chat_id": self.chat_id,
        "first_name": self.first_name,
        "last_name": self.last_name
        }

@app.route("/get_provider_location/<string:provider_id>")
def get_provider_location(provider_id):

    provider = Provider.query.filter_by(provider_id=provider_id).first()
    
    # if provider:
        # change to place_id later
        # return provider.place_id
    
    if provider:
        return jsonify(
            {
                "code": 200,
                "place_id": "place_id:"+provider.place_id

            }
        )
        
    
    return jsonify(
        {
            "code": 404,
            "message": "Provider not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
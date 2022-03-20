from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/requestor'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Requestor(db.Model):
    __tablename__ = 'requestor'

    REQID = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, REQID, full_name, last_name, username, password):
        self.REQID = REQID
        self.full_name = full_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def json(self):
        return {"REQID": self.REQID, "full_name": self.full_name, "last_name": self.last_name, "username": self.username, "password": self.password }

# @app.route("/requestor")
# def who_am_i():
#     return "I am me"

@app.route("/requestor")
def get_all():
    requestor_list = Requestor.query.all()
    if len(requestor_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "requestors": [requestors.json() for requestors in requestor_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no requestors."
        }
    ), 404

@app.route("/requestor/<string:REQID>")
def find_by_REQID(REQID):
    requestor = Requestor.query.filter_by(REQID=REQID).first()
    if requestor:
        return jsonify(
            {
                "code": 200,
                "data": requestor.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Requestor not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020, debug=True)
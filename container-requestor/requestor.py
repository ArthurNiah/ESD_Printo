from cgi import test
from re import X
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

    requestor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    tele_id = db.Column(db.String(64), nullable=False)

    def __init__(self,first_name, last_name, username, tele_id):
        # self.requestor_id = requestor_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.tele_id = tele_id

    def json(self):
        return {"first_name": self.first_name, "last_name": self.last_name, "username": self.username, "tele_id": self.tele_id }

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

@app.route("/requestor/<string:requestor_id>")
def find_by_requestor_id(requestor_id):
    requestor = Requestor.query.filter_by(requestor_id=requestor_id).first()
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

@app.route("/register", methods=['POST'])
def register_requestor():
    # requestor_id = None
    data = request.get_json()
    
    # return(x)
    # return(request.get_json())
    requestor = Requestor(**data)
    try:
        db.session.add(requestor)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the requestor."
            }
        ), 500
 
    return jsonify(
        {
            "code": 201,
            "data": requestor.json()
        }
    ), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
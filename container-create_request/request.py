import os
from flask import Flask, request as req, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:3306/request'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/request'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Request(db.Model):
    __tablename__ = 'request'

    #basic info
    request_id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, nullable= False)
    provider_id = db.Column(db.Integer, nullable= True)
    status = db.Column(db.String(32), nullable=True)
    document_id = db.Column(db.String(100), nullable=True)
    # create_datetime= db.Column(db.Timestamp, nullable= False)

    #gmaps info
    coordinates = db.Column(db.String(100), nullable=True)
    location_name = db.Column(db.String(100), nullable=True)
    place_id = db.Column(db.String(100), nullable=True)

    #for printing info
    color = db.Column(db.String(32), nullable=True)
    no_of_copies = db.Column(db.Integer, nullable=True)
    single_or_double = db.Column(db.String(32), nullable=True)
    size = db.Column(db.String(10), nullable=True)
    comments = db.Column(db.String(100), nullable=True)


    # def __init__(self, requestor_id, provider_id, status, document_link, coordinates, location_name):
#TODO: Try changing the database to Null values upon init
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
    comments = None
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


@app.route("/insert_request", methods=['POST'])
def insert_request():

    data = req.get_json()
    request = Request(data['requestor_id'])

    print(data)

    try:
        db.session.add(request) 
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred updating the request."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": {
                "request_id" : request.request_id,
                "response": request.json()
            },
            "message": "Request has been inserted!"
        }
    ), 201 


@app.route("/get_all_request", methods=['GET'])
def get_all_request():

    try:
        requestList = Request.query.all()
    
        if len(requestList):
            # all_request: []
            # for item in request:
            #     all_request.append(item)
            return jsonify (
                {
                    "code": 200, 
                    "data": {
                        "request":[request.json() for request in requestList]
                    }
                }), 200
        
        return jsonify (
            {
                "code": 404,
                "message": "No requests found in the database."
            }
        ), 404

    except Exception as e:

        return jsonify (
            {
                "code" : 500, 
                "message": "Unable to retrieve requests. Please check error message and try again.",
                "error_message" : str(e)
            }
        ), 500

@app.route("/search_request/<string:request_id>", methods=['GET'])
def search_request(request_id):
    # response = db.session.query('request').filter_by(request_id=request_id)
    
    
    request = Request.query.filter_by(request_id=request_id).first()

    if request:
 
        return jsonify(
            {
                "code": 200,
                "data": {
                    "request_id" : request_id,
                    "response": request.json()
                },
                "message": "Request has been found!"
            }
        ), 200

    else:

        return jsonify (
            {
                "code": 404,
                "message" : "Request with that ID was not found. Please try again!"
            }
        ) , 404

    
@app.route("/update_provider_id/<string:request_id>", methods=['PUT'])
def update_provider_id(request_id):

    try:
        request = Request.query.filter_by(request_id=request_id).first()
        if not request:
            return jsonify(
                {
                    'code': 404, 
                    'data' : request.json(),
                    'message': 'Request not found. Please try again!'
                }
            ), 404

        data = req.get_json()

        if data:
            request.provider_id = data['provider_id']
            db.session.commit()
            return jsonify(
                {
                    'code': 200,
                    "data": {
                        "request_id" : request_id,
                        "response": request.json()
                    },
                    'message' : 'Request has been updated with new provider id.'
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "request_id": request_id
                },
                "message": "An error occurred while updating the request. " + str(e)
            }
        ), 500


@app.route("/update_status/<string:request_id>", methods=['PUT'])
def update_status(request_id):

    try:
        request = Request.query.filter_by(request_id=request_id).first()

        if not request:
            return jsonify(
                {
                    'code': 404, 
                    'data' : request.json(),
                    'message': 'Request not found. Please try again!'
                }
            ), 404

        data = req.get_json()

        if data:
            request.status = data['status']
            db.session.commit()
            return jsonify(
                {
                    'code': 200,
                    "data": {
                        "request_id" : request_id,
                        "response": request.json()
                    },
                    'message' : 'Request has been updated with new status.'
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "request_id": request_id
                },
                "message": "An error occurred while updating the request. " + str(e)
            }
        ), 500


@app.route("/update_document_id/<string:request_id>", methods=['PUT'])
def update_document_id(request_id):

    try:
        request = Request.query.filter_by(request_id=request_id).first()

        if not request:
            return jsonify(
                {
                    'code': 404, 
                    'data' : request.json(),
                    'message': 'Request not found. Please try again!'
                }
            ), 404

        data = req.get_json()
        print(data)
        data = eval(data)

        if data:
            request.document_id = data['doc_id']
            db.session.commit()
            return jsonify(
                {
                    'code': 200,
                    "data": {
                        "request_id" : request_id,
                        "response": request.json()
                    },
                    'message' : 'Request has been updated with new document link.'
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "request_id": request_id
                },
                "message": "An error occurred while updating the request. " + str(e)
            }
        ), 500



@app.route("/update_location/<string:request_id>", methods=['PUT'])
def update_location_name(request_id):

    try:
        request = Request.query.filter_by(request_id=request_id).first()

        if not request:
            return jsonify(
                {
                    'code': 404, 
                    'data' : request.json(),
                    'message': 'Request not found. Please try again!'
                }
            ), 404

        data = req.get_json()

        if data:
            request.location_name = data['location_name']
            request.place_id = data['place_id']
            request.coordinates = data['coordinates']
            db.session.commit()
            return jsonify(
                {
                    'code': 200,
                    "data": {
                        "request_id" : request_id,
                        "response": request.json()
                    },
                    'message' : 'Request has been updated with new location name.'
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "request_id": request_id
                },
                "message": "An error occurred while updating the request. " + str(e)
            }
        ), 500


@app.route("/update_print_details/<string:request_id>", methods=['PUT'])
def update_print_status(request_id):

    try:
        request = Request.query.filter_by(request_id=request_id).first()
        if not request:
            return jsonify(
                {
                    'code': 404, 
                    'data' : request.json(),
                    'message': 'Request not found. Please try again!'
                }
            ), 404

        data = req.get_json()

        if data:
            print(data['color'])
            request.color = data['color']
            request.no_of_copies = data['no_of_copies']
            request.single_or_double = data['single_or_double']
            request.size = data['size']
            request.comments = data['comments']
            db.session.commit()

            return jsonify(
                {
                    'code': 200,
                    "data": {
                        "request_id" : request_id,
                        "response": request.json()
                    },
                    'message' : 'Request has been updated with new printing information.'
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500, 
                "data": {
                    "reqeust_id":request_id
                },
                "message": "An error occurred while updating the request. " + str(e)
            }
            ), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5003, debug=True)
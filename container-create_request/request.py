from flask import Flask, request as req, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/request'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Request(db.Model):
    __tablename__ = 'request'

    #basic info
    request_id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, nullable= False)
    provider_id = db.Column(db.Integer, nullable= True)
    status = db.Column(db.String(32), nullable=True)
    document_link = db.Column(db.String(100), nullable=True)
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

    def __init__(self, requestor_id, status='Unaccepted'):
        self.requestor_id= requestor_id   
        # self.provider_id= provider_id
        self.status= status
        # self.document_link= document_link
        # self.coordinates= coordinates
        # self.location_name = location_name

    def json(self):
        return {
        "requestor_id": self.requestor_id, 
        # "provider_id": self.provider_id, 
        "status": self.status
        # "document_link": self.document_link,
        # "location_name": self.location_name, 
        # "coordinates" : self.coordinates
        }


@app.route("/insert_request", methods=['POST'])
def insert_request():

    # data = req.get_json()
    data = {'requestor_id': 321}
    request = Request(**data)

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

    
@app.route("/update_provider_id/<string:request_id>", methods=['POST'])
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


@app.route("/update_status/<string:request_id>", methods=['POST'])
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


@app.route("/update_document_link/<string:request_id>", methods=['POST'])
def update_document_link(request_id):

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
            request.document_link = data['document_link']
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


@app.route("/update_coordinates/<string:request_id>", methods=['POST'])
def update_coordinates(request_id):

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
            request.coordinates = data['coordinates']
            db.session.commit()
            return jsonify(
                {
                    'code': 200,
                    "data": {
                        "request_id" : request_id,
                        "response": request.json()
                    },
                    'message' : 'Request has been updated with new coordinates.'
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


@app.route("/update_location_name/<string:request_id>", methods=['POST'])
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


if __name__ == '__main__':
    app.run(port=5003, debug=True)
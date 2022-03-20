from email.policy import default
from flask import Flask, request as req, jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/request'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Request(db.Model):
    __tablename__ = 'request'

    request_id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, nullable= False)
    provider_id = db.Column(db.Integer, nullable= False)
    status = db.Column(db.String(32), nullable=False)
    document_link = db.Column(db.String(100), nullable=True)
    # create_datetime= db.Column(db.Timestamp, nullable= False)
    coordinates = db.Column(db.String(100), nullable=False)
    location_name = db.Column(db.String(100), nullable=False)

    def __init__(self, request_id, requestor_id, provider_id, status, document_link, coordinates, location_name):
        self.request_id= request_id
        self.requestor_id= requestor_id   
        self.provider_id= provider_id
        self.status= status
        self.document_link= document_link
        self.coordinates= coordinates
        self.location_name = location_name

    def json(self):
        return {"request_id": self.request_id, "requestor_id": self.requestor_id, "provider_id": self.provider_id, "stauts": self.status, "document_link": self.document_link, "location_name": self.location_name}


@app.route("/insert_request", methods=['POST'])
def insert_request(data):
    if (Request.query.filter_by(request_id=data.rid).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "request_id": data.rid
                },
                "message": "Request already exists."
            }
        ), 400

    data = req.get_json()
    request = Request(data.rid, **data)

    try:
        db.session.add(request) 
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "rid": data.rid
                },
                "message": "An error occurred updating the request."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": request.json(),
            "message": "Request has been inserted!"
        }
    ), 201 




if __name__ == '__main__':
    app.run(port=5000, debug=True)
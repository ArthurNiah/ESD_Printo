from flask import Flask, request as req, jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/esdeez'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Request(db.Model):
    __tablename__ = 'request'

    rid = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), nullable=False)
    reqid= db.Column(db.Integer, nullable= False)
    ppid= db.Column(db.Integer, nullable= True)
    docid= db.Column(db.Integer, nullable= False)
    teleid= db.Column(db.String(64), nullable= False)

    def __init__(self, rid, reqid, ppid, status, docid, teleid):
        self.rid= rid
        self.reqid= reqid   
        self.ppid= ppid
        self.status= status
        self.docid= docid
        self.teleid= teleid

    def json(self):
        return {"rid": self.rid, "status": self.status, "reqid": self.reqid, "ppid": self.ppid, "docid": self.docid, "teleid": self.teleid}


@app.route("/request/<string:rid>", methods=['POST'])

def create_request(rid):
    if (Request.query.filter_by(rid=rid).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "rid": rid
                },
                "message": "Request already exists."
            }
        ), 400

    data = req.get_json()
    request = Request(rid, **data)

    try:
        db.session.add(request) 
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "rid": rid
                },
                "message": "An error occurred updating the request."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": request.json() 
        }
    ), 201 




if __name__ == '__main__':
    app.run(port=5000, debug=True)
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

# db = SQLAlchemy(app)

CORS(app)  

class Request(db.Model):
    __tablename__= 'request'

    request_id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, nullable=False)
    doc_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # modified = db.Column(db.DateTime, nullable=False,
    #                     default=datetime.now, onupdate=datetime.now)


    def json(self):
        dto = {
            'request_id': self.request_id,
            'requestor_id': self.requestor_id,
            'doc_id': self.doc_id,
            'created': self.created
        }

        dto['request_item'] = []
        for oi in self.request_item:
            dto['request_item'].append(oi.json())

        return dto


class Request_item(db.Model):
    __tablename__ = 'request_item'

    request = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.ForeignKey(
        'request.request_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    book_id = db.Column(db.String(13), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # order_id = db.Column(db.String(36), db.ForeignKey('order.order_id'), nullable=False)
    # order = db.relationship('Order', backref='order_item')
    order = db.relationship(
        'Order', primaryjoin='Order_Item.order_id == Order.order_id', backref='order_item')

    def json(self):
        return {'item_id': self.item_id, 'book_id': self.book_id, 'quantity': self.quantity, 'order_id': self.order_id}


from flask import Flask, request as req, jsonify
from flask_cors import CORS
import os, sys
import requests


# import amqp_setup
# import pika
import json

#import internal files
from invokes import invoke_http
# from google_maps import get_current_location

app = Flask(__name__)
CORS(app)


price_list = {
    "A4": 1.0, 
    "A3": 1.0, 
    "non_color" : 1.0, 
    "color" : 1.0, 
    "base_price" : 2.00, 
    "copy_price" : 1.00
}


@app.route("/payment", methods=["GET"])
def cal_payment():

    request = req.get_json()
    if request:
        try:
            color = request['color']
            copies = int(request['no_of_copies'])
            size = request['size']

            final_price = price_list['base_price'] + price_list[color] + price_list[size] + copies*price_list['copy_price']
            return jsonify (
                {
                    "code": 200, 
                    "message": "Final price microservice success", 
                    "data": {
                        "final_price": final_price, 
                        "response": request
                    }
                }
            ), 200

        except Exception as e:

            return jsonify({
                "code": 500, 
                "message": "Final price microservice failed:" + str(e), 
                "data": {
                    "response":request
                }
            }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=True)
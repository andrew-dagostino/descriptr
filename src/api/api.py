"""Implement Flask and provide endpoints to interact with Descriptr."""

import os
from flask import Flask
from flask import jsonify
from flask import request
from classes.descriptr import Descriptr
import json

""" Change working directory to here """
os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
dcptr = Descriptr()


@app.route("/")
def root():
    """
    List available endpoints in the API.

    Returns:
        (flask.response): A response with a JSON body of available endpoints.
    """
    return jsonify({'available_endpoints': ["/search"]})


@app.route("/search", methods=['GET', 'POST'])
def search():
    """
    GET available search filters. POST searches to Descriptr.

    Returns:
        (flask.response): A response with a JSON body of filters or courses.
    """
    if request.method == 'GET':
        # Make a list of methods of Decriptr that start with 'do_search_'
        searches = [method for method in dir(dcptr) if method.startswith("do_search_")]
        endpts = map(lambda x: x.replace("do_search_", "", 1), searches)
        return jsonify({'available_filters': list(endpts)})

    ret = json.loads(dcptr.apply_filters(request.get_json()))
    return jsonify(ret)


# @app.errorhandler(400)
# def bad_req(e):
#     return jsonify(error=str(e)), 400
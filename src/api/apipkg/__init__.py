"""Implement Flask and provide endpoints to interact with Descriptr."""

import os
from flask import Flask
from flask import jsonify
from flask import request
from classes.descriptr import Descriptr
import json

""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))


def create_app(test_config=None):
    app = Flask(__name__)
    dcptr = Descriptr()

    @app.route("/")
    def root():
        """
        List available endpoints in the API.

        Returns:
            (flask.response): A response with a JSON body of available endpoints.
        """
        return jsonify({'available_endpoints': ["/search", "/prerequisite"]})

    @app.route("/search", methods=['GET', 'POST'])
    def search():
        """
        GET available search filters. POST searches to Descriptr.

        Returns:
            (flask.response): A response with a JSON body of filters or courses.
        """
        if request.method == 'GET':
            # Make a list of methods of Decriptr that start with 'do_search_'
            searches = [method for method in dir(
                dcptr) if method.startswith("do_search_")]
            endpts = map(lambda x: x.replace("do_search_", "", 1), searches)
            return jsonify({'available_filters': list(endpts)})

        results = json.loads(dcptr.apply_filters(request.get_json()))
        status = 200 if results["error"] is None else 400
        return jsonify(results), status

    @app.route("/prerequisite/<course_id>", methods=['GET'])
    def prerequisite_search(course_id):
        """
        GET tree of prerequisites for a course by course id (eg. CIS-2750)

        Args:
            - course_id (string)    Id of a course with a hyphen (eg. CIS-2750 instead of CIS*2750)

        Returns:
            (flask.response): A response with a JSON body courses
        """
        try:
            dcptr.do_search_course_prerequisites({
                'query': course_id.replace("-", "*").upper(),
                'comparison': None
            })
            results = json.loads(dcptr.export_json())
            status = 200 if results["error"] is None else 400
        except Exception as e:
            status = 400
            results = {
                'courses': [],
                'error': str(e)
            }

        return jsonify(results), status

    return app

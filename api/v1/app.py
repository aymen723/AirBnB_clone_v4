#!/usr/bin/python3
""" Flask framwork app """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ to close the storage """
    storage.close()


@app.errorhandler(404)
def error_notfound(error):
    """ 404 
    ---
    responses:
      404:the path or ressource was not found    """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    h = environ.get('HBNB_API_HOST')
    p = environ.get('HBNB_API_PORT')
    if not h:
        h = '0.0.0.0'
    if not p:
        p = '5000'
    app.run(host=h, port=p, threaded=True)

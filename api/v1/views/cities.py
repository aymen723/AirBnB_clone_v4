#!/usr/bin/python3
""" file objects to hundle the api calls for the cities  """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def All_cities(state_id):
    """
    api func to get all cities
    """
    lcities = []
    s = storage.get(State, state_id)
    if not s:
        abort(404)
    for city in s.cities:
        lcities.append(city.to_dict())

    return jsonify(lcities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    api func to fetch city by ID
    """
    c = storage.get(City, city_id)
    if not c:
        abort(404)
    return jsonify(c.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    api func to delete a city by ID
    """
    c = storage.get(City, city_id)

    if not c:
        abort(404)
    storage.delete(c)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],strict_slashes=False)
def post_city(state_id):
    """
    a func to create a city
    """
    s = storage.get(State, state_id)
    if not s:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    d = request.get_json()
    instance = City(**d)
    instance.state_id = s.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    a api func to patch the city by ID
    """
    c = storage.get(City, city_id)
    if not c:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(c, key, value)
    storage.save()
    return make_response(jsonify(c.to_dict()), 200)

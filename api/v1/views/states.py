#!/usr/bin/python3
""" file objects to hundle the api calls for the states  """
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """
    api function to get alll states
    """
    allstates = storage.all(State).values()
    lstates = []
    for s in allstates:
        lstates.append(s.to_dict())
    return jsonify(lstates)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ get a state by ID """
    s = storage.get(State, state_id)
    if not s:
        abort(404)

    return jsonify(s.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    delete a state by ID
    """

    s = storage.get(State, state_id)

    if not s:
        abort(404)

    storage.delete(s)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    d = request.get_json()
    instance = State(**d)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def patch_state(state_id):
    """
    api function to patch the state
    """
    s = storage.get(State, state_id)

    if not s:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    skips = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in skips:
            setattr(s, key, value)
    storage.save()
    return make_response(jsonify(s.to_dict()), 200)

#!/usr/bin/python3
""" file objects to hundle the api calls for the Users  """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """
    a api action to get all the users 
    """
    allusers = storage.all(User).values()
    lusers = []
    for user in allusers:
        lusers.append(user.to_dict())
    return jsonify(lusers)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ get user by id """
    u = storage.get(User, user_id)
    if not u:
        abort(404)

    return jsonify(u.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],strict_slashes=False)
def delete_user(user_id):
    """
    delete a user by id
    """

    u = storage.get(User, user_id)

    if not u:
        abort(404)

    storage.delete(u)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    a api to create a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    d = request.get_json()
    instance = User(**d)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def patch_user(user_id):
    """
    a api call to patch a user
    """
    u = storage.get(User, user_id)

    if not u:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    skip = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in skip:
            setattr(u, key, value)
    storage.save()
    return make_response(jsonify(u.to_dict()), 200)

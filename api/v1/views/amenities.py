#!/usr/bin/python3
""" file objects to hundle the api calls for the amenities  """
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def All_amenities():
    """
    fetch all amentites
    """
    allameni = storage.all(Amenity).values()
    lamenities = []
    for amenity in allameni:
        lamenities.append(amenity.to_dict())
    return jsonify(lamenities)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],strict_slashes=False)
def get_amenity(amenity_id):
    """ api func to get amenity by ID """
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)

    return jsonify(a.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],strict_slashes=False)
def delete_amenity(amenity_id):
    """
     api func to delete an amenity by ID
    """

    a = storage.get(Amenity, amenity_id)

    if not a:
        abort(404)

    storage.delete(a)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    api func to create amenity
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    d = request.get_json()
    instance = Amenity(**d)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],strict_slashes=False)
def patch_amenity(amenity_id):
    """
    api func to patch an amenity by ID
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    skips = ['id', 'created_at', 'updated_at']

    a = storage.get(Amenity, amenity_id)

    if not a:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in skips:
            setattr(a, key, value)
    storage.save()
    return make_response(jsonify(a.to_dict()), 200)

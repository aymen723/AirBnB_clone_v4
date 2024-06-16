#!/usr/bin/python3
""" file objects to hundle the api calls for the placesamenitites  """
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request


@app_views.route('places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def All_place_amenities(place_id):
    """
    fetchh all placesamenitites
    """
    p = storage.get(Place, place_id)

    if not p:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        a = [amenity.to_dict() for amenity in p.amenities]
    else:
        a = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in p.amenity_ids]

    return jsonify(a)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    api func to delete amenity by ID
    """
    p = storage.get(Place, place_id)

    if not p:
        abort(404)

    a = storage.get(Amenity, amenity_id)

    if not a:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if a not in p.amenities:
            abort(404)
        p.amenities.remove(a)
    else:
        if amenity_id not in p.amenity_ids:
            abort(404)
        p.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],strict_slashes=False)
def Create_place_amenity(place_id, amenity_id):
    """
    api func to link a palce to amenity by ID
    """
    p = storage.get(Place, place_id)

    if not p:
        abort(404)

    a = storage.get(Amenity, amenity_id)

    if not a:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if a in p.amenities:
            return make_response(jsonify(a.to_dict()), 200)
        else:
            p.amenities.append(a)
    else:
        if amenity_id in p.amenity_ids:
            return make_response(jsonify(a.to_dict()), 200)
        else:
            p.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(a.to_dict()), 201)

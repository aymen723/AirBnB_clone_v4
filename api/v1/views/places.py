#!/usr/bin/python3
""" file objects to hundle the api calls for the places  """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],strict_slashes=False)
def All_places(city_id):
    """
    api func to fetchh all places by city ID
    """
    c = storage.get(City, city_id)

    if not c:
        abort(404)

    lpalces = [place.to_dict() for place in c.places]

    return jsonify(lpalces)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    fetch palce by ID
    """
    p = storage.get(Place, place_id)
    if not p:
        abort(404)

    return jsonify(p.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],strict_slashes=False)
def delete_place(place_id):
    """
    api func to delete a place
    """

    p = storage.get(Place, place_id)

    if not p:
        abort(404)

    storage.delete(p)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    api func to create a palce by city ID
    """
    c = storage.get(City, city_id)

    if not c:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    d = request.get_json()
    u = storage.get(User, d['user_id'])

    if not u:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    d["city_id"] = city_id
    instance = Place(**d)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def patch_place(place_id):
    """
    a function to patch palce by city ID
    """
    p = storage.get(Place, place_id)

    if not p:
        abort(404)

    d = request.get_json()
    if not d:
        abort(400, description="Not a JSON")

    skips = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in d.items():
        if key not in skips:
            setattr(p, key, value)
    storage.save()
    return make_response(jsonify(p.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    api func to search places
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    d = request.get_json()

    if d and len(d):
        s = d.get('states', None)
        c = d.get('cities', None)
        a = d.get('amenities', None)

    if not d or not len(d) or (
            not s and
            not c and
            not a):
        places = storage.all(Place).values()
        lplaces = []
        for place in places:
            lplaces.append(place.to_dict())
        return jsonify(lplaces)

    lplaces = []
    if s:
        s = [storage.get(State, s_id) for s_id in s]
        for state in s:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            lplaces.append(place)

    if c:
        city_obj = [storage.get(City, c_id) for c_id in c]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in lplaces:
                        lplaces.append(place)

    if a:
        if not lplaces:
            lplaces = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in a]
        lplaces = [place for place in lplaces
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in lplaces:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)

#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Reviews """
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],strict_slashes=False)
def All_reviews(place_id):
    """
    api call to fetch all reviews
    """
    p = storage.get(Place, place_id)

    if not p:
        abort(404)

    lReviews = [review.to_dict() for review in p.reviews]

    return jsonify(lReviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    to fetch a reiview by ID
    """
    r = storage.get(Review, review_id)
    if not r:
        abort(404)

    return jsonify(r.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],strict_slashes=False)
def delete_review(review_id):
    """
    api func to delete a review
    """

    r = storage.get(Review, review_id)

    if not r:
        abort(404)

    storage.delete(r)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],strict_slashes=False)
def create_review(place_id):
    """
    a function to create a review
    """
    p = storage.get(Place, place_id)

    if not p:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    d = request.get_json()
    u = storage.get(User, d['user_id'])

    if not u:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    d['place_id'] = place_id
    instance = Review(**d)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def patch_review(review_id):
    """
    api call to patch the review
    """
    r = storage.get(Review, review_id)

    if not r:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    skips = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in skips:
            setattr(r, key, value)
    storage.save()
    return make_response(jsonify(r.to_dict()), 200)

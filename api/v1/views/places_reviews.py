#!/usr/bin/python3
"""
View for Place objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def retrive_all_reviews(place_id=None):
    """"Retrieves the list of all Reviews objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    return jsonify([Review.to_dict(review) for review in reviews]), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retrive_review(review_id=None):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(Review.to_dict(review)), 200


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id=None):
    """" Deletes a Review object and returns an
    empty dict and 200 as the status"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id=None):
    """" Creates a Review object"""
    request_json = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request_json:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User,  request_json.get('user_id'))
    if not user:
        abort(404)
    if 'text' not in request_json:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    review = Review(**request_json)
    review.place_id = place_id
    review.save()
    return make_response(jsonify(Review.to_dict(review)), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """" Updates a Review object"""
    request_json = request.get_json()
    if request_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request_json.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(Review.to_dict(review)), 200)

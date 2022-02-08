#!/usr/bin/python3
"""reviews and endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_all_reviews(place_id=None):
    """
        get reviews relate with a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    return jsonify([Review.to_dict(review) for review in reviews]), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review_id(review_id=None):
    """
        get review based on its id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(Review.to_dict(review)), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id=None):
    """
        Deletes a review based on its id and returns an empty JSON
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id=None):
    """
        Stores with id and returns a review in a given place
    """
    review_object = request.get_json(silent=True)
    if not review_object:
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if 'user_id' not in review_object:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, review_object.get('user_id'))
    if not user:
        abort(404)
    if 'text' not in review_object:
        return jsonify({'error': 'Missing text'}), 400
    review_object['place_id'] = place_id
    review = Review(**review_object)
    review.save()
    return jsonify(Review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id=None):
    """
        Returns the data of a given review
    """
    keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    review_object = request.get_json(silent=True)
    if review_object is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    for key, val in review_object.items():
        if key not in keys:
            setattr(review, key, val)
    review.save()
    return make_response(jsonify(Review.to_dict(review)), 200)

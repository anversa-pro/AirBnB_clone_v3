#!/usr/bin/python3
"""
View for Place objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id=None):
    """
    Returns the all stored places of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places_in_city = city.places
    return jsonify([Place.to_dict(place) for place in places_in_city]), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id=None):
    """
    Returns a specific Place given an object id 
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(Place.to_dict(place)), 200


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """
    Deletes a Place given an id and returns an empty JSON
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id=None):
    """
    Creates a Place object
    """
    jrequest = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if jrequest is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in jrequest:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user = storage.get(User,  jrequest.get('user_id'))
    if not user:
        abort(404)
    if 'name' not in jrequest:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place = Place(**jrequest)
    place.city_id = city_id
    place.save()
    return make_response(jsonify(Place.to_dict(place)), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """"
    Updates a Place object
    """
    jrequest = request.get_json()
    if jrequest is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in jrequest.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(Place.to_dict(place)), 200)

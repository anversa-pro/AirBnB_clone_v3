#!/usr/bin/python3
""" state module api v1 """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def get_all_cities(state_id=None):
    """
        Returns all Cities
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities_in_state = state.cities
    return jsonify([City.to_dict(city) for city in cities_in_state]), 200


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_cities_by_id(city_id=None):
    """
        Returns an specific city given an id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(City.to_dict(city)), 200


@app_views.route('cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """
        Deletes a state with id and returns an empty JSON
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id=None):
    """" Creates a City object"""
    jrequest = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if jrequest is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in jrequest:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city = City(**jrequest)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(State.to_dict(city)), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """" Updates a City object"""
    jrequest = request.get_json()
    if jrequest is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in jrequest.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(State.to_dict(city)), 200)

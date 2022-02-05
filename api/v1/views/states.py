#!/usr/bin/python3
""" state module api v1 """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
    """
        Returns all States objects
    """
    return jsonify([user.to_dict() for user in
                    storage.all(State).values()]), 200


@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """
        All states or one state of method GET and returns
        all state objects
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """
        Deletes a state with id and returns an empty JSON
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """
        Stores and returns a new state
    """
    reqst = request.get_json(silent=True)
    if reqst is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in reqst:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**reqst)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id=None):
    """
        Return the information of a given state
    """
    keys = ['id', 'created_at', 'updated_at']
    reqst = request.get_json(silent=True)

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not reqst:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, val in reqst.items():
        if key not in keys:
            setattr(state, key, val)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)

#!/usr/bin/python3
"""
Script to set Json status return
"""

from api.v1.views import app_views

from models import storage
from flask import jsonify


@app_views.route('/status')
def status_route():
    """
    Method that returns a Json Status OK
    """
    return (jsonify({'status': 'OK'}))


@app_views.route('/stats')
def stat_route():
    """
    Method that returns the count of each object
    """
    return (jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                     "places": storage.count("Place"),
                     "reviews": storage.count("Review"),
                     "states": storage.count("State"),
                     "users": storage.count("User")
                     }))

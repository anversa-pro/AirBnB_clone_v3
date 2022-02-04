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

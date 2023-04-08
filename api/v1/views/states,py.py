#!/usr/bin/python3

"""
State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import Flask, jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def del_states(state_id):
    """deletes a state object"""
    if


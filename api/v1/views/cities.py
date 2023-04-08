#!/usr/bin/python3
"""city endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """get cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    cities_db = storage.all(City).values()
    for city in cities_db:
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities), 200


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """get a specific city"""
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_cities(city_id):
    """Deletes a specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>', methods=['POST'], strict_slashes=False)
def creates_cities(city_id):
    """transform the HTTP body request to a dictionary"""
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': "Not a JSON"}), 400
        name = data.get('name', None)

        if not name:
            return jsonify({'error': 'Missing name'}), 400
        data['state_id'] = state_id
        city = City(**data)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Updates a City object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())

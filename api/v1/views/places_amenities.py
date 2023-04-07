#!/usr/bin/python3
"""city endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities(place_id):
    """get all amenities in a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    amenities_db = storage.all(Amenity).values()
    for amenity in amenities_db:
        if amenity.place_id == place_id:
            amenities.append(amenity.to_dict())
    return jsonify(amenities), 200
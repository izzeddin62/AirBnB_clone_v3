#!/usr/bin/python3

"""
place endpoint
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City

@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                    strict_slashes=False)
def get_all_reviews(place_id):
    """get all reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

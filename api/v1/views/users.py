#!/usr/bin/python3
"""users endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """get users"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """get a specific user"""
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete one user"""
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """create a new user"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'email' not in request.json:
        abort(400, "Missing email")
    if 'password' not in request.json:
        abort(400, "Missing password")
    user = User(**request.json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update one user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

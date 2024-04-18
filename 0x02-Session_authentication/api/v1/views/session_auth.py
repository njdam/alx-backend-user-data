#!/usr/bin/env python3
""" A new Flask view that handles all routes for the Session authentication
"""
from flask import jsonify, request
from os import getenv
from typing import Tuple

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """ Retrieve and verify email and password from user inputs
    POST /api/v1/auth_session/login
    Return:
      - JSON representation of a User object.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(users[0], 'id'))
        response = jsonify(users[0].to_json())
        response.set_cookie(getenv("SESSION_NAME"), session_id)
        return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        '/api/v1/auth_session/logout', methods=['DELETE'], strict_slashes=False
        )
def logout() -> Tuple[str, int]:
    """ Deleting the Session ID contains in the request as cookie
    DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200

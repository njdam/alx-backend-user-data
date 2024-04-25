#!/usr/bin/env python3
""" Basic Flask app!
"""

from flask import Flask, jsonify
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index() -> str:
    """ Route handler for the root URL
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Route handler for registering a new user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

#!/usr/bin/env python3
""" A hasing of password in user authentications
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ A function that hash a password
    """
    salt = bcrypt.gensalt()
    hash_passwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_passwd


class Auth:
    """ Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ A registration of a user
        Args:
            email (str): Email of the user
            password (str): Password of the user

        Returns:
            User: The newly created User object

        Raises:
            ValueError: If a user with the given email already exists
        """
        try:
            # Check if a user with the given email already exists
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass  # No user found, continue with registration

        # Hash the password
        hashed_password = _hash_password(password)

        # Save the user to the database
        user = self._db.add_user(email, hashed_password)

        return user

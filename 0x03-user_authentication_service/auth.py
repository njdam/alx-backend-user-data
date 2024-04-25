#!/usr/bin/env python3
""" A hasing of password in user authentications
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """ A function that hash a password
    """
    salt = bcrypt.gensalt()
    hash_passwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_passwd

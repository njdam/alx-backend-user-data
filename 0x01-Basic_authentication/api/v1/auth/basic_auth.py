#!/usr/bin/env python3
""" A file with a class for authenticating management
"""
import re
import base64
import binascii
from typing import TypeVar, Tuple

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ A class inherits from Auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """
        "Extracts the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            matched = re.fullmatch(pattern, authorization_header.strip())
            if matched:
                return matched.group('token')
        return None

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
        """ Extracts the Base64 part of the Authorization header for a Basic
        Authentication!
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            matched = re.fullmatch(pattern, authorization_header.strip())
            if matched:
                return matched.group('token')
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """ Decode Base64 string to return decoded value
        """
        if type(base64_authorization_header) == str:
            try:
                decoded = base64.b64decode(
                        base64_authorization_header,
                        validate=True
                        )
                return decoded.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """ Basic - User credentials
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            matched = re.fullmatch(
                pattern, decoded_base64_authorization_header.strip(),
            )
            if matched:
                user = matched.group('user')
                password = matched.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """ Retrieving user instance according to the user_email and pwd
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieving User instance for a request with API fully protected
        by a complete Basic authentication
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)

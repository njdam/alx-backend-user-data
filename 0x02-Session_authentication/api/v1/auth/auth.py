#!/usr/bin/env python3
""" A python file for managing the API authentication
"""

from typing import List, TypeVar
from flask import request
import re


class Auth:
    """ A class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ A public method to check if path is excluded
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '/':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)

                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ A public method to request headers for Authorization
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ A public method to request Current User
        """
        return None

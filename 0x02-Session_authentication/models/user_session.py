#!/usr/bin/env python3
""" A file for sessions in database for users
"""

from models.base import Base


class UserSession(Base):
    """ A class that inherits from Base
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialization of UserSession class instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

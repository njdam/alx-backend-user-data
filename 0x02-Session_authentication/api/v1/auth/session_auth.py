#!/usr/bin/env python3
""" A file with a class SessionAuth that inherits from Auth.
"""

from uuid import uuid4

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ A class SessionAuth that inherits from Auth.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ An instance method that create session id for a user_id
        """
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

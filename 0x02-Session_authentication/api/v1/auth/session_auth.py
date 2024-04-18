#!/usr/bin/env python3
""" A file with a class SessionAuth that inherits from Auth.
"""

from uuid import uuid4

from api.v1.auth.auth import Auth
from models.user import User


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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ An instance method that returns a User ID based on a Session ID
        """
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """ An instance method that returns a User instance based on
        a cookie value
        """
        if request is not None:
            _my_session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(_my_session_id)
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """ An instance method that deletes the user session / logout
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if request is None or session_id is None or user_id is None:
            return False
        if session_id in self.user_id_for_session_id:
            del self.user_id_for_session_id[session_id]
        return True

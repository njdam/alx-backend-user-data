#!/usr/bin/env python3
""" A file with a class SessionExpAuth that inherits from SessionAuth
"""
from os import getenv
from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ A class SessionExpAuth that inherits from SessionAuth
    """
    def __init__(self):
        """ Initialization of SessionExpAuth class
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Creation of session_id by user_id
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Retrieving user_id by associated session_id
        """
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            current_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            expected_time = session_dict['created_at'] + time_span
            if expected_time < current_time:
                return None
            return session_dict['user_id']

#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.

        If echo=True shows all engine creation processes
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Implemented function for adding user!

        Args:
            email (str): Email of the user
            hashed_password (str): Hashed password of the user

        Returns:
            User: The newly created User object
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Find a user by the given keyword arguments

        Args:
            **kwargs: Arbitrary keyword arguments for filtering the user

        Returns:
            User: The first user found matching the provided criteria

        Raises:
            NoResultFound: If no user is found matching the criteria
            InvalidRequestError: If wrong query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> User:
        """ Update a user's attributes

        Args:
            user_id (int): The ID of the user to update
            **kwargs: Arbitrary keyword arguments for updating the user's
            attributes

        Raises:
            ValueError: If an argument that does not correspond to a user
            attribute is passed
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        updates = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                updates[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            updates,
            synchronize_session=False,
        )
        self._session.commit()

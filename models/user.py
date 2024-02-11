#!/usr/bin/python3
"""The script defines the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """To represent a User.

    Attributes:
        email (str): The email of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        password (str): The password of the user.

    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

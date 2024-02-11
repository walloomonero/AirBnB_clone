#!/usr/bin/python3
"""The script defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """To represent a city.

    Attributes:
        name (str): The name of the city.
        state_id (str): The state id.
    """

    state_id = ""
    name = ""

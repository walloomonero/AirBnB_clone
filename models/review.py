#!/usr/bin/python3
"""The script defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a review.

    Attributes:
        user_id (str): The User id.
        text (str): The text of the review.
        place_id (str): The Place id.
    """ 

    place_id = ""
    user_id = ""
    text = ""

#!/usr/bin/env python3
""" Person module
"""
from dataclasses import dataclass
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import db


@dataclass
class Person(db.Model):
    """ Person class
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    @staticmethod
    def validate_id(person_id: int) -> bool:
        """ Verify Person ID is a valid integer
        Args:
            person_id (int): Person instance auto-generated database ID
        Return:
            True (bool): person_id is valid, positive integer
            False (bool): person_id is not a valid, non-negative integer
        """
        if person_id and person_id > 0 and isinstance(person_id, int):
            return True
        return False
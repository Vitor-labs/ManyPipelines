"""
Module Docstring
"""

from abc import ABCMeta, abstractmethod
from typing import Dict


class DBRepositoryInterface(metaclass=ABCMeta):
    """
    This class defines the interface for a database repository.

    Methods:
        insert_record(data: Dict) -> None: Inserts an record into database.
    """

    @classmethod
    @abstractmethod
    def insert_record(cls, flag: str, data: Dict) -> None:
        """
        Inserts a new row into the database 'nhtsa_data' repository.

        Args:
            flag (str): A flag to determine the type of data being inserted.
            data (DataDictType): A dictionary containing the data to be inserted.

        Raises:
            Any database-related exceptions that might occur during the insertion process.
        """
        raise NotImplementedError("DBRepository.insert_complaints: not implemented")

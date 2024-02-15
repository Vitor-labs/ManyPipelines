"""
This module defines 
"""

from typing import Dict

from src.infra.db_connection import DBConnector
from src.infra.interfaces.db_repository import DBRepositoryInterface


class DBRepository(DBRepositoryInterface):
    """
    Implementation of the DBRepositoryInterface for database
    operations.
    """

    @classmethod
    def insert_record(cls, flag: str, data: Dict) -> None:
        """
        Inserts a new row into the database 'nhtsa_data' repository.

        Args:
            flag (str): A flag to determine the type of data being inserted.
            data (DataDictType): A dictionary containing the data to be inserted.

        Raises:
            Any database-related exceptions that might occur during the insertion process.
        """
        query = f"""
        INSERT INTO {flag.lower()} (
            {', '.join(data.keys())}
        ) VALUES (
            {', '.join('?' * len(data))}
        )
        """
        cursor = DBConnector.local.cursor()  # Only testing, use conn later.
        cursor.execute(query, tuple(data.values()))
        DBConnector.local.commit()

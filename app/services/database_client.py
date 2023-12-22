import os
import logging
from pymongo import MongoClient
from ..config import Config


class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


class DatabaseClient:
    """
    A database client for performing operations on a MongoDB database.
    It initializes a connection to the database using a URI obtained from environment variables.
    """

    def __init__(self):
        """
        Initializes the database client and connects to the default database specified in MONGODB_URI.
        """
        try:
            self.logger = logging.getLogger(__name__)
            self.client = MongoClient(Config.MONGODB_URI)
            self.db = self.client.get_default_database()
        except Exception as e:
            # Handle connection-related exceptions and log the error
            self.logger.exception(f"Database Connection Error: {str(e)}")
            raise ConnectionError(f"Database Connection Error: {str(e)}")

    def save_message(self, message: dict) -> None:
        """
        Saves a message to the 'messages' collection in the database.
        :param message: A dictionary representing the message to be saved.
        """
        try:
            self.db.messages.insert_one(message)
        except Exception as e:
            # Handle insertion-related exceptions and log the error
            self.logger.exception(f"Database Insertion Error: {str(e)}")
            raise DatabaseError(f"Database Insertion Error: {str(e)}")

    def get_all_messages(self) -> list:
        """
        Retrieves all messages from the 'messages' collection in the database.
        :return: A list of dictionaries where each dictionary is a message from the database.
        """
        try:
            return list(self.db.messages.find({}))
        except Exception as e:
            # Handle query-related exceptions and log the error
            self.logger.exception(f"Database Query Error: {str(e)}")
            raise DatabaseError(f"Database Query Error: {str(e)}")

    def close_connection(self):
        """
        Closes the database connection when it's no longer needed.
        """
        if hasattr(self, 'client'):
            self.client.close()

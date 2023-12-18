import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file


class DatabaseClient:
    """
    A database client for performing operations on a MongoDB database.
    It initializes a connection to the database using a URI obtained from environment variables.
    """

    def __init__(self):
        """
        Initializes the database client and connects to the default database specified in MONGODB_URI.
        """
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client.get_default_database()

    def save_message(self, message: dict) -> None:
        """
        Saves a message to the 'messages' collection in the database.
        :param message: A dictionary representing the message to be saved.
        """
        self.db.messages.insert_one(message)

    def get_all_messages(self) -> list:
        """
        Retrieves all messages from the 'messages' collection in the database.
        :return: A list of dictionaries where each dictionary is a message from the database.
        """
        return list(self.db.messages.find({}))

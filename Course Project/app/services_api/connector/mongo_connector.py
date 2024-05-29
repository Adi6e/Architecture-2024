from pymongo import MongoClient


class MongoDB:

    def __init__(self):
        username = "root"
        password = "example"
        mongo_uri = f"mongodb://{username}:{password}@mongo:27017/"
        self.client = MongoClient(mongo_uri)
        self.db = self.client["arch"]
        self.collection = self.db["reports"]

    def get_client(self):
        return self.client

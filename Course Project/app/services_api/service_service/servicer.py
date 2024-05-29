from bson.objectid import ObjectId
from connector.mongo_connector import MongoDB


class ServiceService:

    def __init__(self):
        self.client = MongoDB().get_client()
        self.db = self.client["arch"]
        self.collection = self.db["services"]

    def create_service(self, title, description, creator_id):
        _data = {
            "title": title,
            "description": description,
            "creator_id": creator_id
        }
        result = self.collection.insert_one(_data)
        return str(result.inserted_id)

    def read_service(self, service_id):
        service = self.collection.find_one({"_id": ObjectId(service_id)})
        if service:
            service['_id'] = str(service['_id'])
        return service

    def read_user_services(self, creator_id):
        services = self.collection.find({"creator_id": creator_id})
        response = []
        for i in services:
            i['_id'] = str(i['_id'])
            response.append(i)
        return response

    def update_service(self, service_id, title=None, description=None, creator_id=None):
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if creator_id is not None:
            update_data["creator_id"] = creator_id

        result = self.collection.update_one(
            {"_id": ObjectId(service_id)}, {"$set": update_data})
        if result.modified_count > 0:
            updated_service = self.collection.find_one(
                {"_id": ObjectId(service_id)})
            updated_service["_id"] = str(updated_service["_id"])
            print(updated_service)
            return updated_service
        else:
            updated_service = self.collection.find_one(
                {"_id": ObjectId(service_id)})
            if updated_service:
                return 1
            else:
                return 0

    def delete_service(self, service_id):
        result = self.collection.delete_one({"_id": ObjectId(service_id)})
        return result.deleted_count > 0

from bson.objectid import ObjectId
from connector.mongo_connector import MongoDB


class OrderCRUD:
    def __init__(self):
        self.client = MongoDB().get_client()
        self.db = self.client["arch"]
        self.collection = self.db["orders"]

    def read_all(self):
        response = []
        for i in self.collection.find():
            # print(i)
            conf = {}
            conf['_id'] = str(i['_id'])
            conf['name'] = str(i["name"])
            response.append(conf)
        return response

    def create_order(self, order_data: dict):
        inserted_order = self.collection.insert_one(order_data)
        return str(inserted_order.inserted_id)

    def read_order(self, order_id: str):
        order = self.collection.find_one({"_id": ObjectId(order_id)})
        if order:
            order['_id'] = str(order['_id'])
            for i in range(len(order['services'])):
                order['services'][i] = str(order['services'][i])
        return order

    def update_order(self, order_id: str, updated_data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": updated_data}
        )
        return result.modified_count

    def delete_order(self, order_id: str):
        result = self.collection.delete_one({"_id": ObjectId(order_id)})
        return result.deleted_count

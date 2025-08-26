from bson import ObjectId
from datetime import datetime, timezone
from config.database import db_config

class BaseModel:

    collection_name = None

    def __init__(self, **data):
        self._id = data.get('_id', ObjectId())
        self.created_at = data.get('created_at', datetime.now(timezone.utc))
        self.updated_at = data.get('updated_at', None)
        
        for key, value in data.items():
            setattr(self, key, value)

    def validate(self):
        pass

    def to_dict(self):
        data = self.__dict__.copy()
        data['_id'] = str(self._id)
        data['created_at'] = self.created_at.isoformat()
        return data
    
    def save(self):

        self.validate()
        self.updated_at = datetime.now(timezone.utc)

        collection = db_config.get_collection(self.collection_name)
        data = self.to_dict()

        collection.replace_one({'_id': self._id}, data, upsert=True)
        return str(self._id)
    
    def delete(self):
        collection = db_config.get_collection(self.collection_name)
        result = collection.delete_one({'_id': self._id})
        return result.deleted_count > 0
    
    @classmethod
    def find_one(cls, filter_dict):
        collection = db_config.get_collection(cls.collection_name)
        data = collection.find_one(filter_dict)
        if data:
            return cls(**data)
        return None

    @classmethod
    def find_many(cls, filter_dict={}):
        collection = db_config.get_collection(cls.collection_name)
        docs = collection.find(filter_dict)
        return [cls(**doc) for doc in docs]

    @classmethod
    def update(cls, filter_dict, update_data):
        collection = db_config.get_collection(cls.collection_name)
        result = collection.update_one(filter_dict, {"$set": update_data})
        return result.modified_count > 0

import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

class DatabaseConfig:

    def __init__(self):
        self._client = None
        self._db = None

        # self.MONGODB_URI = os.getenv('MONODB_URI', 'mongodb://localhost:27017/')
        self.MONGODB_URI = os.getenv('MONODB_URI', 'mongodb+srv://prajapatiarjun2801:760097@cluster0.nkwapof.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        self.DATABASE_NAME = os.getenv('DATABASE_NAME', 'RideHailingDeskAppTkinter')
        self.CONNECT_TIMEOUT = int(os.getenv('CONNECT_TIMEOUT', 5000)) 
        self.SERVER_SELECTION_TIMEOUT = int(os.getenv('SERVER_SELECTION_TIMEOUT', 5000))

    def connect(self):
        if self._client is None:
            self._client = MongoClient(
                self.MONGODB_URI,
                connectTimeoutMS = self.CONNECT_TIMEOUT,
                serverSelectionTimeoutMS = self.SERVER_SELECTION_TIMEOUT
            )
            self._db = self._client[self.DATABASE_NAME]
            print(f"Connected to database: {self.DATABASE_NAME}")
        return self._db
    
    def disconnect(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("Disconnected from database")
    
    def get_database(self):
        try:
            if self._db is None:
                return self.connect()
        except ServerSelectionTimeoutError as e:
            print(f"Database connection error: {e}")
            self.connect()
        return self._db
    
    def get_collection(self, collection_name):
        db = self.get_database()
        return db[collection_name]

db_config = DatabaseConfig()
import pymongo

# client = pymongo.MongoClient(['localhost:27017'])
# database = client['test']
# database['student'].insert({"Name":"Brian", "Age":"28", "Height":"173"})

class Database(object):
    URI = ['localhost:27017']
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['project']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def fine_distinct(collection, query, tag):
        return Database.DATABASE[collection].find(query).distinct(tag)

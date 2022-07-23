from pymongo import MongoClient
import pymongo

class Database:
    def __init__(self):
        CONNECTION_STRING = "mongodb+srv://test:test123@cluster0.nqyvkqz.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(CONNECTION_STRING)
        self.dbname = self.client['aircraft_details']
        self.collections = self.dbname['details']
        
    def get_database(self):
        return self.dbname
    
    def get_collections(self):
        return self.collections

    def insert_doc(self, name, id, passengers, runway_number, landing_time):
        print(name, id, passengers, runway_number, landing_time)
        if isinstance(name, str) and isinstance(passengers, int) and isinstance(runway_number, int) and isinstance(landing_time, str) and isinstance(id, int):
            self.collections.insert_many([
                {
                    "name":name, 
                    "id": id, 
                    "passengers": passengers, 
                    "runway_number": runway_number, 
                    "landing_time": landing_time
                }
                ])
        else:
            raise Exception("Please check input format")
    
    def get_data(self):
        details = self.collections.find()
        return details


import sys
from pymongo import MongoClient

class ychatdb:
    def __init__(self,param) -> None:
        self.host= param['host']
        self.db_name = param['database']
        print(self.host)
        client = MongoClient(self.host)
        print("Test")
        self.client = client
        self.db=client[self.db_name]
        #return(client)

    def getDatabases(self):
        return(self.client.list_database_names)

    def getCollection(self):
        return(self.client[self.db_name])

    def getDocument(self,collection):
        col = self.db[collection]
        return (col.find({}))


        



    


    




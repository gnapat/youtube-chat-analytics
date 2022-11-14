
import sys
from pymongo import MongoClient

class ychatdb:
    def __init__(self,param) -> None:
        self.host= param['host']
        self.db_name = param['database']
        #print(self.host)
        #client = MongoClient("mongodb+srv://appadm:e7Eddf7fe7Eddf7f@cluster0.g7t88xt.mongodb.net/?retryWrites=true&w=majority" , 
        #                    tls=True,
        #                    tlsAllowInvalidCertificates=True)

        client = MongoClient( self.host, 
                            tls=True,
                            tlsAllowInvalidCertificates=True)
                            
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

    def getGroupName(self,collection):
        collec = self.db[collection]
        i = collec.aggregate([{ '$group': {'_id': '$aname','Sum':{'$sum':1}}},{"$sort": {"Sum":-1}}])

        return(i)
    
    def getGroupVid(self,collection):
        collec = self.db[collection]
        i = collec.aggregate([{ '$group': {'_id': '$vid','Sum':{'$sum':1}}}])

        return(i)

    def getChList(self):
        collec = self.db['info']
        re = collec.find({})
        return(re)
    
    def getChCodeByTitleTh(self,name):
        collec = self.db['info']
        colch = self.db['cliplist']
        re = collec.find({"title_th":name})
        record = re[0]
        #print(record['chl_code'])
        re = colch.find({"code":record['chl_code']})
        #for i in re:
        #    print(i)
        #print(re)
        return(re)

    def getChByTitleTh(self,chname,ep):
        collec = self.db['info']
        colch = self.db['cliplist']

        re = colch.find({"org_name_th":chname,'title_th':ep[0]})
        r =re[0]
        #for i in re:
        #    print(i)
        aa={"org_name_th":chname,'title_th':ep[0]}
        col = self.db[r['code']]
        chdata = col.find({"vid":r['vid']})
        return(chdata)


        



    


    




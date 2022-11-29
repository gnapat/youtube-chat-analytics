
import sys
from pymongo import MongoClient
import pymongo

class ychatdb:
    def __init__(self,param) -> None:
        self.host= param['host']
        self.db_name = param['database']

        try:
            client = MongoClient( self.host, 
                            tls=True,
                            tlsAllowInvalidCertificates=True)
        except pymongo.errors.ConnectionFailure as e:
            print ("Could not connect: %s" %(e))
        except pymongo.errors.ServerSelectionTimeoutErro as e:
             print ("Could not connect: %s" %(e))
        except:
            print("Error!!!!??")
             

                            
        print("Test")
        self.client = client
        self.db=client[self.db_name]
        #return(client)
    
    def addNewChannel(self,code,name):
        info=self.db['info']
        #print(f"Check {code}")
        ret = info.find({'chl_code':code})

        cc=0
        alist = []
        for i in ret:
            alist.append(i)
            cc += 1
        
        if alist !=[]:
            return(-1)
        else:
            record={'chl_code':code,'title_th':name,'title_en':''}
            info.insert_one(record)
            return(0)

    def addNewProgram(self,code,name,program):
        colch = self.db['cliplist']
        record={"code":code,"vid":"9GXSL5bgPII","org_name_th":name,"org_name_en":"","title_th":program,"title_en":""}
        colch.insert_one(record)

    def putMsg(self,code,name,program,record_list):
        col = self.db[code]
        colch = self.db['cliplist']
        cc = 0
        ssize = 10
        l = []
        for i in record_list:
            record={"datetime":i['datetime'],"vid":i['vid'],"aname":i['aname'],"msg":i['msg']}
            l.append(record)
            cc += 1
        
        col.insert_many(l)

        data = l[0]
        record={"code":code,"vid":data['vid'],"org_name_th":name,"org_name_en":"","title_th":program,"title_en":""}
        colch.insert_one(record)







    def removeChannel(self,code):
        info=self.db['info']
        print(f"Check {code}")
        ret = info.find({'chl_code':code})

        cc=0
        alist = []
        for i in ret:
            alist.append(i)
            
            cc += 1
        
        if alist !=[]:
            record={'chl_code':code}
            info.delete_one(record)
            return(1)
        else:

            return(0)
        

        #for i in ret:
        #    print(i)
        #record={'chl_code':code,'title_th':name,'title_en':''}
        #info.insert_one(record)

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
        try:
            re = collec.find({})
        except pymongo.errors.ExecutionTimeout as e:
             print ("Could not find: %s" %(e))
             re = None
        except pymongo.errors.ServerSelectionTimeoutErro as e:
             print ("Could not connect: %s" %(e))
        except:
            print("Error!!!!")
        
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

        col = self.db[r['code']]
        chdata = col.find({"vid":r['vid']})
        return(chdata)

    def getCodeByCh(self,chname):
        collec = self.db['info']
        #colch = self.db['cliplist']

        re = collec.find({"title_th":chname})
        r =re[0]
        #print(r)
        return(r['chl_code'])

    def renameProgram(self,chname,curr_progm,new_progm):
        collec = self.db['info']
        colch = self.db['cliplist']


        re = colch.find({"org_name_th":chname,'title_th':curr_progm})
        ri = re[0]
        colch.update_one({'_id':ri['_id']}, {"$set": {"title_th":new_progm }})



        

    

    


    




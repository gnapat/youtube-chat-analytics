
import sys
from pymongo import MongoClient
sys.path.insert(0, '/home/gz/project/nlp/lookvchat/lib/python3.9/site-packages')

import pytchat

chl = sys.argv[1]
title=sys.argv[2]
vid = sys.argv[3]
#client = MongoClient()
client = MongoClient("mongodb+srv://appadm:e7Eddf7fe7Eddf7f@cluster0.g7t88xt.mongodb.net/?retryWrites=true&w=majority")
mydatabase = client['YouTubeChat']
collection = mydatabase[chl]

#chl_info = mydatabase['channel_info']

chat = pytchat.create(video_id=vid)
while chat.is_alive():
    for c in chat.get().sync_items():

        record = {'datetime': c.datetime,\
                'vid': vid, \
                'aname': c.author.name, \
                'msg': c.message} 
        print(record)
        rec = collection.insert_one(record)
        #print(rec)

        #print(record)
        #print(f"{{c.datetime}} [{c.author.name}]- {c.message}")
        #print(c)
        #print("{\"datetime\":\"%s\",\"channel\":\"%s\",\"title\":\"%s\",\"aname\":\"%s\",\"msg\":\"%s\"}" %(c.datetime,chl,title,c.author.name,c.message))


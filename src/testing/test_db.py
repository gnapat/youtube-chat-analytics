
import sys
import configparser

#sys.path.insert(0, '/home/gz/project/nida/ychat/youtube-chat-analytics/src/include/')
sys.path.insert(0, 'src/include/')

from ychat_db  import ychatdb
from config import ychat_config as yconf
 
yc = yconf("C:\\Users\\LEGION\\work\\project\\nida\\youtube-chat-analytics\\src\\testing\\config.conf")
y = yc.getconfig()
#aa = y['Test01']
aa = y['mongodb.net']
#print(aa['host'])
#print(aa['database'])



dbconf={"host":aa['host'],"database":aa['database']}
#print(dbconf)
client = ychatdb(dbconf)
#client.getCollection("YouTubeChat")
aa = client.getDocument('info')
for i in aa:
    print(i['title_th'])
"""
ret = client.getGroupVid("A00011")
cc = 0
for i in ret:
    if (cc > 9):
        break

    print(i)

    cc+=1
"""





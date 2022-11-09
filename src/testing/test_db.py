
import sys
import configparser

#sys.path.insert(0, '/home/gz/project/nida/ychat/youtube-chat-analytics/src/include/')
sys.path.insert(0, 'src/include/')

from ychat_db  import ychatdb
from config import ychat_config as yconf
 
yc = yconf("config.conf")
y = yc.getconfig()
aa = y['Test01']
#print(aa['host'])
#print(aa['database'])



dbconf={"host":aa['host'],"database":aa['database']}
print(dbconf)
client = ychatdb(dbconf)
#client.getCollection("YouTubeChat")

ret = client.getGroupVid("A00011")
cc = 0
for i in ret:
    if (cc > 9):
        break

    print(i)

    cc+=1





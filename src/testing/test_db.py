
import sys
#sys.path.insert(0, '/home/gz/project/nida/ychat/youtube-chat-analytics/src/include/')
sys.path.insert(0, 'src/include/')

from ychat_db  import ychatdb

la = {"host":"mongodb+srv://appadm:e7Eddf7fe7Eddf7f@cluster0.g7t88xt.mongodb.net/?retryWrites=true&w=majority",
        "database":"YouTubeChat"}
client = ychatdb(la)
#client.getCollection("YouTubeChat")

ret = client.getDocument("A00011")
cc = 0
for i in ret:
    if (cc > 9):
        break

    print(i)

    cc+=1





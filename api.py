from borg import *
from config import *
from models import *

# API handler class
class API(Borg):
    def __init__(self):
        Borg.__init__(self)

        if not self._assimilated:
            self.videoList = list()
            self.forceVideo = False
            self.messageList = list()
            self._assimilated = True

    def addVideoID(self, vidID, instantly=False):
        v = Video(vidID).toDict()

        if instantly is True:
            if v in self.videoList:
                self.videoList.remove(v)
            self.forceVideo = v["vidID"]
        elif instantly is not True and v not in self.videoList:
            self.videoList.append(v)

    def apiVideoList(self):
        return self.videoList

    def apiNextVideo(self):
        if len(self.videoList) > 0:
            return self.videoList.pop(0)["vidID"]
        else:
            return str()

    def apiAddMessage(self, sender, body):
        m = Message(sender, body).toDict()
        self.messageList.append(m)
        return m

    def apiState(self):
        obj = dict()
        if self.forceVideo is not False:
            obj["forceVideo"] = self.forceVideo
            self.forceVideo = False
        if len(self.messageList) > 0:
            obj["messageList"] = list(self.messageList)
            self.messageList.clear()
        if len(self.videoList) > 0:
            obj["videoList"] = self.videoList
        return obj

    def checkKey(self, key):
        if (key != Config().key()):
            return False
        else:
            return True


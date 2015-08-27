from extractors import *

# Video model
class Video():
    def __init__(self, vidID):
        self.vidID = vidID
        self.name = NameExtractor(vidID).extract()

    def toDict(self):
        d = dict()
        d["vidID"] = self.vidID
        d["name"] = self.name
        return d

# Message model
class Message():
    def __init__(self, sender, body):
        self.sender = sender
        self.body = body

    def toDict(self):
        d = dict()
        d["sender"] = self.sender
        d["body"] = self.body
        return d


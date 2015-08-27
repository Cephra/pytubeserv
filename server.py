#!/usr/bin/python3

import http.server
import os
import json
from urllib.parse import parse_qs
from models import *
from config import *

# API handler class
class PyTubeAPI():
    def __init__(self):
        self.videoList = list()
        self.forceVideo = False
        self.messageList = list()

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


class PyTubeServHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        http.server.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def send_json(self, data):
        self.wfile.write(bytes(json.dumps(data), "UTF-8"))

    def send_plain(self, data):
        self.wfile.write(bytes(data, "UTF-8"))

    def deny_access(self):
        self.send_response(403)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.send_plain("Access denied.")

    def grant_access(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/json")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/"):
            ## AUTH

            path = query = None
            query = self.path.split("?")
            if len(query) > 1:
                path = query[0]
                query = parse_qs(query[1])
                if not tubeapi.checkKey(query["apiKey"][0]):
                    self.deny_access()
                    return
                else:
                    self.grant_access()
            else:
                self.deny_access()
                return

            ## API

            if path == "/api/list":
                self.send_json(tubeapi.apiVideoList())

            elif path == "/api/next":
                self.send_json(tubeapi.apiNextVideo())

            elif path == "/api/state":
                self.send_json(tubeapi.apiState())

            elif path == "/api/add":
                videoID = query["videoID"][0]
                force = True if (query["force"][0] == "1") else False
                tubeapi.addVideoID(videoID, force)
                self.send_json("Added {} to list".format(videoID))

            elif path == "/api/message":
                msgSender = query["sender"][0]
                msgBody = query["body"][0]
                self.send_json(tubeapi.apiAddMessage(msgSender, msgBody))

            else:
                self.send_json("Unknown API node")

        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    Config()
    addr = ("", 1234)

    tubeapi = PyTubeAPI()
    httpd = http.server.HTTPServer(addr, PyTubeServHandler)

    os.chdir("./player")
    httpd.serve_forever()

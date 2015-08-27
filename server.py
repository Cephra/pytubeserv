#!/usr/bin/python3

import http.server
import os
import json
from urllib.parse import parse_qs
from config import *
from api import *

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
                if not API().checkKey(query["apiKey"][0]):
                    self.deny_access()
                    return
                else:
                    self.grant_access()
            else:
                self.deny_access()
                return

            ## API

            if path == "/api/list":
                self.send_json(API().apiVideoList())

            elif path == "/api/next":
                self.send_json(API().apiNextVideo())

            elif path == "/api/state":
                self.send_json(API().apiState())

            elif path == "/api/add":
                videoID = query["videoID"][0]
                force = True if (query["force"][0] == "1") else False
                API().addVideoID(videoID, force)
                self.send_json("Added {} to list".format(videoID))

            elif path == "/api/message":
                msgSender = query["sender"][0]
                msgBody = query["body"][0]
                self.send_json(API().apiAddMessage(msgSender, msgBody))

            else:
                self.send_json("Unknown API node")

        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    Config()

    httpd = http.server.HTTPServer(("", 1234), PyTubeServHandler)
    os.chdir("./player")
    httpd.serve_forever()

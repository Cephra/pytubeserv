from http.client import HTTPSConnection
from html.parser import HTMLParser
from gzip import GzipFile
import re

class NameExtractor():
    def __init__(self, vidID):
        conn = HTTPSConnection("www.youtube.com")

        conn.request("GET", "/watch?v={}".format(vidID))

        stream = conn.getresponse()
        if stream.getheader("Content-Encoding") is not None:
            stream = GzipFile(fileobj=stream)
        self.data = str(stream.read(), "utf-8")

        conn.close()

    def extract(self):
        ms = re.findall(r"<title>(.*)\s-\sYouTube</title>", self.data)
        p = HTMLParser()
        if ms:
            return p.unescape(ms[0])
        else:
            return ""



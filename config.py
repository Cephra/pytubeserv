import os
import json

class Config():
    __borg = {}

    def __init__(self):
        self.__dict__ = self.__borg

        if not hasattr(self, "_config"):
            if os.path.isfile("config.json"):
                # read config
                with open("config.json", mode="r") as f:
                    self._config = json.loads(f.read())
                print("Read config.json")
            else:
                # generate config
                with open("config.json", mode="w") as f:
                    d = {}
                    d["key"] = input("What API key shall be used? ")
                    self._config = d
                    f.write(json.dumps(d,
                        indent=2,
                        separators=(",", ": "),
                        sort_keys=True)+"\n")
                print("Saved config.json")

    def key(self):
        return self._config["key"]


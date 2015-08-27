class Borg():
    __borg = {}
    _assimilated = False

    def __init__(self):
        self.__dict__ = self.__borg

from .msg import message
from ..fundamental.ints import bigsizeInt
from ..abstract.init_data import InitData


class InitMessage(message):
    def __init__(self, raw):
        self.raw = raw

    def decode(self):
        self.type = bigsizeInt(self.raw[:4])
        self.type.decode()
        self.data = InitData(self.raw[4:])
        self.data.decode()

    def encode(self):
        pass

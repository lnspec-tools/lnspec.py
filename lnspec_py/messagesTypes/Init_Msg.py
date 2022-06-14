from .msg import message
from ..fundamental.ints import bigsizeInt
from ..abstract.init_data import InitData


class InitMessage(message):
    """
    The message init is encoded like
    1. Types
    2. Data
    3. tlv_stream
    """

    def __init__(self, raw):
        self.raw = raw

    def decode(self):
        self.type = bigsizeInt(self.raw[:4])
        self.type.decode()
        self.data = InitData(self.raw[4:])
        self.data.decode()

    def encode(self):
        pass

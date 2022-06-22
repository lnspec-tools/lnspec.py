import logging

from .msg import message
from ..fundamental.ints import u16Int
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
        logging.info(f"Int message hex type: {self.raw[:4]}")
        self.type = u16Int(self.raw[:4])
        self.type.decode()
        logging.debug(f"Init message hex data: {self.raw[4:]}")
        self.data = InitData(self.raw[4:])
        self.data.decode()

    def encode(self) -> str:
        self.type.encode()
        return f"{self.type.val.hex()}{self.data.encode()}"

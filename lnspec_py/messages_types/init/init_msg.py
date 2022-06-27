import logging

from lnspec_py.messages_types.msg import Message
from lnspec_py.basic_type.ints import u16Int
from lnspec_py.messages_types.init.init_data import InitData


class InitMessage(Message):
    """
    The message init is encoded like
    1. Types
    2. Data
    3. tlv_stream
    """

    def __init__(self, msg_type: u16Int, data: InitData, name: str = "init"):
        self.name = name
        self.type = msg_type
        self.data = data

    @staticmethod
    def decode(raw_msg: str) -> "InitMessage":
        logging.debug(f"Int message hex type: {raw_msg[:4]}")
        type = u16Int(raw_msg[:4])
        type.decode()
        logging.debug(f"Init message hex data: {raw_msg[4:]}")
        data = InitData.decode(raw_msg=raw_msg[4:])
        return InitMessage(msg_type=type, data=data)

    def encode(self) -> str:
        self.type.encode()
        return f"{self.type.val.hex()}{self.data.encode()}"

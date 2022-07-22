from curses import raw
import logging

from lnspec_py.message_type.msg import Message
from lnspec_py.basic_type.int import U16Int
from lnspec_py.message_type.init.init_data import InitData


class InitMessage(Message):
    """
    The message init is encoded like
    1. Types
    2. Data
    3. tlv_stream
    """

    def __init__(self, msg_type: U16Int, data: InitData, name: str = "init"):
        self.name = name
        self.type = msg_type
        self.data = data

    @staticmethod
    def decode(raw_msg: str) -> "InitMessage":
        logging.debug(f"Int message hex type: {raw_msg}")
        type, raw_msg = U16Int.decode_with_hex_str(raw_msg)
        logging.debug(f"Init message hex data: {raw_msg}")
        data = InitData.decode(raw_msg=raw_msg)
        return InitMessage(msg_type=type, data=data)

    def encode(self) -> str:
        self.type.encode()
        return f"{self.type.val.hex()}{self.data.encode()}"

"""
This class is for the pong control Message
as specify in https://github.com/lightning/bolts/blob/master/01-messaging.md#control-messages
"""

import logging
from typing import List
from lnspec_py.basic_type.int import u16Int
from lnspec_py.basic_type.bitmask import Bitfield
from lnspec_py.basic_type.hex_type import ChannelId
from lnspec_py.message_type.msg import Message


class PongMessage(Message):
    """
    The message Pong is encoded like
    [u16: type]
    [u16:num_pong_bytes]
    [u16:byteslen]
    [byteslen*byte:ignored]
    """

    def __init__(
        self,
        msg_type: u16Int,
        bytesLen: u16Int,
        ignored: List[int],
    ) -> None:
        self.msg_type = msg_type
        self.name = "pong"
        self.bytesLen = bytesLen
        self.ignored = ignored

    @staticmethod
    def decode(raw_msg: str) -> "PongMessage":
        """
        Decode the Pong message data from a raw hex message
        """

        msg_type = u16Int(raw_msg[:4])
        msg_type.decode()
        raw_msg = raw_msg[4:]
        bytesLen = u16Int(raw_msg[:4])
        bytesLen.decode()
        raw_msg = raw_msg[4:]
        ignored = Bitfield.decode(raw_msg[: bytesLen.val * 2])
        return PongMessage(msg_type, bytesLen, ignored)

    def encode(self) -> str:
        ignored = ""
        if len(self.ignored) > 0:
            ignored = Bitfield.encode(self.ignored)
        else:
            ignored = "00" * self.bytesLen.val

        self.msg_type.encode()
        self.bytesLen.encode()
        return self.msg_type.val.hex() + self.bytesLen.val.hex() + ignored

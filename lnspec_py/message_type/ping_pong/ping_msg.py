"""
This class is for the ping control Message
as specify in https://github.com/lightning/bolts/blob/master/01-messaging.md#control-messages
"""

import logging
from typing import List
from lnspec_py.basic_type.int import u16Int
from lnspec_py.basic_type.bitmask import Bitfield
from lnspec_py.basic_type.hex_type import ChannelId
from lnspec_py.message_type.msg import Message


class PingMessage(Message):
    """
    The message Ping is encoded like
    [u16: type]
    [u16:num_pong_bytes]
    [u16:byteslen]
    [byteslen*byte:ignored]
    """

    def __init__(
        self,
        msg_type: u16Int,
        numPongBytes: u16Int,
        bytesLen: u16Int,
        ignored: List[int],
    ) -> None:
        self.msg_type = msg_type
        self.name = "ping"
        self.numPongBytes = numPongBytes
        self.bytesLen = bytesLen
        self.ignored = ignored

    @staticmethod
    def decode(raw_msg: str) -> "PingMessage":
        """
        Decode the Ping message data from a raw hex message
        """
        msg_type, raw_msg = u16Int.decode_with_hex_str(raw_msg)
        numPongBytes, raw_msg = u16Int.decode_with_hex_str(raw_msg)
        bytesLen, raw_msg = u16Int.decode_with_hex_str(raw_msg)
        ignored = Bitfield.decode(raw_msg[: bytesLen.val * 2])
        return PingMessage(msg_type, numPongBytes, bytesLen, ignored)

    def encode(self) -> str:
        ignored = ""
        if len(self.ignored) > 0:
            ignored = Bitfield.encode(self.ignored)
        else:
            ignored = "00" * self.bytesLen.val

        self.msg_type.encode()
        self.numPongBytes.encode()
        self.bytesLen.encode()
        return (
            self.msg_type.val.hex()
            + self.numPongBytes.val.hex()
            + self.bytesLen.val.hex()
            + ignored
        )

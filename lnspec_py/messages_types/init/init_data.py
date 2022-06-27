"""
This class is for the Data section of Init Message
as specify in https://github.com/lightning/bolts/blob/master/01-messaging.md#the-init-message
"""
import logging
from typing import List
from lnspec_py.basic_type.ints import u16Int
from lnspec_py.basic_type.bitmask import Bitfield
from lnspec_py.messages_types.tvl_record import TVLRecord


class InitData:
    """
    The Data section of message init is encoded like
    1. gflen - u16
    2. globalfeatures - gflen*byte (in hex digit * 2)
    3. flen - u16
    4. features - flen *byte (in hex digit * 2)
    5. tlvs - init_tlvs
    """

    def __init__(
        self,
        gflen: u16Int,
        global_features: List[int],
        flen: u16Int,
        features: List[int],
        tvl_stream: TVLRecord,
    ) -> None:
        self.name = "init"
        self.gflen = gflen
        self.global_features = global_features
        self.flen = flen
        self.features = features
        self.tvl_stream = tvl_stream

    @staticmethod
    def decode(raw_msg: str) -> "InitData":
        """
        Decode the init message data from a raw hex message message
        """
        # Take the first 4 hex digit (are 2 bytes) to decode the size f the global feature encoding
        gflen = u16Int(raw_msg[:4])
        gflen.decode()
        # if glen > 0, it mean global features field is not empty
        # first convert raw hex str to int, then convert it to bitfield and
        # finally we assert if the size of globalfeatures is equal to the size specify in gflen
        global_features = []
        if gflen.val > 0:
            tmp = raw_msg[4 : 4 + (gflen.val * 2)]
            logging.debug(f"global feature hex {tmp}")
            global_features = Bitfield.decode(tmp)

        # Get the start index of feln by getting end position of global features
        flenStart = 4 + (gflen.val * 2)
        # Get the end index of flen by adding 8 as u16 is 2 bytes and there is 4 hex digit in 2 bytes
        flenEnd = (gflen.val * 2) + 8
        # get the raw msg part of flen
        flen = u16Int(raw_msg[flenStart:flenEnd])
        flen.decode()
        # if flen > 0, it mean features field is not empty
        # first convert raw hex str to int, then convert it to bitfield
        # where value indicate the index of bit is on or off
        features = []
        if flen.val > 0:
            tmp = raw_msg[flenEnd : flenEnd + (flen.val * 2)]
            features = Bitfield.decode(tmp)
        tvl_stream = TVLRecord(raw_msg[flenEnd + flen.val * 2 :])
        tvl_stream.decode()
        return InitData(
            gflen=gflen,
            global_features=global_features,
            flen=flen,
            features=features,
            tvl_stream=tvl_stream,
        )

    def encode(self) -> str:
        # Here we check if glfen value > 0
        # if yes, then we convert global features back to hex str
        # first we convert bitfield to decimal int
        # then we pad 0s in front if len(str)%2 != 0
        global_features = ""
        if len(self.global_features) > 0:
            global_features = Bitfield.encode(self.global_features)
        # Here we check if flen value > 0
        # if yes, then we convert global features back to hex str
        # first we convert bitfield to decimal int
        # then we pad 0s in front if len(str)%2 != 0
        features = ""
        if len(self.features) > 0:
            features = Bitfield.encode(self.features)

        self.tvl_stream.encode()
        self.gflen.encode()
        self.flen.encode()
        assert len(self.gflen.val) == 2
        assert len(self.flen.val) == 2
        return (
            self.gflen.val.hex()
            + global_features
            + self.flen.val.hex()
            + features
            + self.tvl_stream.encoded
        )

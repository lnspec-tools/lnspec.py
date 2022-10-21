"""
This class is for the Data section of Init Message
as specify in https://github.com/lightning/bolts/blob/master/01-messaging.md#the-init-message
"""
import logging
from typing import List
from lnspec_py.basic_type.int import U16Int
from lnspec_py.basic_type.bitmask import Bitfield
from lnspec_py.basic_type.tvl_record import TVLRecord


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
        gflen: U16Int,
        global_features: List[int],
        flen: U16Int,
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
        # if glen > 0, it mean global features field is not empty
        # first convert raw hex str to int, then convert it to bitfield and
        # finally we assert if the size of globalfeatures is equal to the size specify in gflen
        global_features, raw_msg = Bitfield.decode_with_len(raw_msg)
        features, raw_msg = Bitfield.decode_with_len(raw_msg)
        tvl_stream = TVLRecord(raw_msg)
        tvl_stream.decode()
        return InitData(
            gflen=global_features.size,
            global_features=global_features.bitfield,
            flen=features.size,
            features=features.bitfield,
            tvl_stream=tvl_stream,
        )

    def encode(self) -> str:
        global_features = ""
        if len(self.global_features) > 0:
            global_features = Bitfield.encode(self.global_features)
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

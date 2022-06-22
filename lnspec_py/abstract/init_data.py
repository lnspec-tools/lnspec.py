"""
This class is for the Data section of Init Message
as specify in https://github.com/lightning/bolts/blob/master/01-messaging.md#the-init-message
"""
from ..fundamental.ints import u16Int, bigsizeInt
from lnspec_py.basic_type.bitmask import Bitfield
from .tvl_record import TVLRecord
from ..utils.utils import (
    int_to_bitfield,
    bitfield_to_int,
    pad_zero_Hex,
)


class InitData:
    """
    The Data section of message init is encoded like
    1. gflen - u16
    2. globalfeatures - gflen*byte (in hex digit * 2)
    3. flen - u16
    4. features - flen *byte (in hex digit * 2)
    5. tlvs - init_tlvs
    """

    def __init__(self, raw) -> None:
        self.raw = raw
        self.encoded = None
        self.globalFeatures = []
        self.features = []

    def decode(self):
        self.gflen = u16Int(self.raw[:4])
        self.gflen.decode()
        # if glen > 0, it mean global features field is not empty
        # first convert raw hex str to int, then convert it to bitfield and
        # finally we assert if the size of globalfeatures is equal to the size specify in gflen
        if self.gflen.val > 0:
            tmp = self.raw[4 : 4 + (self.gflen.val * 2)]
            tmp = int(tmp, 16)
            self.globalFeatures = int_to_bitfield(tmp)[::-1]
            self.globalFeatures = [
                i
                for i in range(len(self.globalFeatures))
                if self.globalFeatures[i] != 0
            ]
            # assert len(self.globalFeatures) // 8 == self.gflen.val

        # Get the start index of feln by getting end position of global features
        flenStart = 4 + (self.gflen.val * 2)
        # Get the end index of flen by adding 8 as u16 is 2 bytes and there is 4 hex digit in 2 bytes
        flenEnd = (self.gflen.val * 2) + 8
        # get the raw msg part of flen
        self.flen = u16Int(self.raw[flenStart:flenEnd])
        self.flen.decode()
        # if flen > 0, it mean features field is not empty
        # first convert raw hex str to int, then convert it to bitfield and
        # finally we assert if the size of features is equal to the size specify in flen
        if self.flen.val > 0:
            tmp = self.raw[flenEnd : flenEnd + (self.flen.val * 2)]
            tmp = int(tmp, 16)
            self.features = int_to_bitfield(tmp)[::-1]
            self.features = [
                i for i in range(len(self.features)) if self.features[i] != 0
            ]
            # assert len(self.features) // 8 == self.flen.val
        self.tvl_stream = TVLRecord(self.raw[flenEnd + self.flen.val * 2 :])
        self.tvl_stream.decode()

    def encode(self):
        # Here we check if glfen value > 0
        # if yes, then we convert global features back to hex str
        # first we convert bitfield to decimal int
        # then we pad 0s in front if len(str)%2 != 0
        # finally we assert the len(str) / 2 == gflen.val
        if self.gflen.val > 0:
            self.globalFeatures = bitfield_to_int(self.globalFeatures)
            self.globalFeatures = bytes.fromhex(
                pad_zero_Hex(hex(self.globalFeatures)[2:])
            ).hex()
            # assert len(self.globalFeatures) / 2 == self.gflen.val
        else:
            self.globalFeatures = ""
        # Here we check if flen value > 0
        # if yes, then we convert global features back to hex str
        # first we convert bitfield to decimal int
        # then we pad 0s in front if len(str)%2 != 0
        # finally we assert the len(str) / 2 == flen.val
        if self.flen.val > 0:
            self.features = bitfield_to_int(self.features)
            self.features = bytes.fromhex(pad_zero_Hex(hex(self.features)[2:])).hex()
            # assert len(self.features) / 2 == self.flen.val
        else:
            self.features = ""
        self.tvl_stream.encode()
        self.gflen.encode()
        self.flen.encode()
        assert len(self.gflen.val) == 2
        assert len(self.flen.val) == 2
        return (
            self.gflen.val.hex()
            + self.globalFeatures
            + self.flen.val.hex()
            + self.features
            + self.tvl_stream.encoded
        )

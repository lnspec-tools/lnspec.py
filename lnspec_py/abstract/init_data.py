from pyexpat import features
from ..fundamental.ints import u16Int, bigsizeInt
from .tvl_record import TVLRecord


"""
This class is for the Data section of Init Message 
as specify in https://github.com/lightning/bolts/blob/master/01-messaging.md#the-init-message
"""


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
        self.globalFeatures = None
        self.features = None

    def decode(self):
        self.gflen = u16Int(self.raw[:4])
        self.gflen.decode()
        if self.gflen.val > 0:
            length = len(self.raw[4 : 4 + (self.gflen.val * 2)])
            if length % 4 != 0:
                # here we pad 0s in the beginning due to the fact bytes.fromHex() only take in hex string which len%4 == 0
                tmp = "0" * abs(4 - length) + self.raw[4 : 4 + (self.gflen.val * 2)]
            else:
                tmp = self.raw[4 : 4 + (self.gflen.val * 2)]
            self.globalFeatures = bigsizeInt(tmp)
            self.globalFeatures.decode()
        # Get the start index of feln by getting end position of global features
        flenStart = 4 + (self.gflen.val * 2)
        # Get the end index of flen by adding 8 as u16 is 2 bytes and there is 4 hex digit in 2 bytes
        flenEnd = (self.gflen.val * 2) + 8
        self.flen = u16Int(self.raw[flenStart:flenEnd])
        self.flen.decode()
        if self.raw[flenEnd : flenEnd + self.flen.val]:
            length = len(self.raw[flenEnd : flenEnd + (self.flen.val * 2)])
            # here we need to pads 0s in front if len%4 != 0
            if length % 4 != 0:
                tmp = (
                    "0" * (length % 4)
                    + self.raw[flenEnd : flenEnd + (self.flen.val * 2)]
                )
            else:
                tmp = self.raw[flenEnd : flenEnd + (self.flen.val * 2)]
            self.features = bigsizeInt(tmp)
            self.features.decode()
        self.tvl_stream = TVLRecord(self.raw[flenEnd + self.flen.val * 2 :])
        self.tvl_stream.decode()

    def encode(self):
        if self.gflen.val > 0:
            self.globalFeatures.encode()
            if len(self.globalFeatures.val) > 1:
                assert (
                    len(self.globalFeatures.val) - (len(self.globalFeatures.val) - self.gflen.val) == self.gflen.val
                    == self.gflen.val
                )
            else:
                assert len(self.globalFeatures.val) == self.gflen.val
            # There are 2 hex number in a bytes and since we assume the input string is hex that's why glen.val * 2
            self.globalFeatures.val = str(self.globalFeatures.val.hex())[
                -self.gflen.val * 2 :
            ]
        else:
            # make globalFeatues empty if gflen is 0
            self.globalFeatures.val = ""
        if self.flen.val > 0:
            self.features.encode()
            print(self.features.val)
            print(self.flen.val, "hi")
            if len(self.features.val) > 1:
                assert len(self.features.val) - (len(self.features.val) - self.flen.val) == self.flen.val
            else:
                assert len(self.features.val) == self.flen.val
            # we need to remove the 0 padding in front
            self.features.val = str(self.features.val.hex())[-self.flen.val * 2 :]
        else:
            self.features.val = ""
        self.tvl_stream.encode()
        self.gflen.encode()
        self.flen.encode()
        assert len(self.gflen.val) == 2
        assert len(self.flen.val) == 2
        self.encoded = (
            str(self.gflen.val.hex())
            + self.globalFeatures.val
            + str(self.flen.val.hex())
            + self.features.val
            + self.tvl_stream.encoded
        )

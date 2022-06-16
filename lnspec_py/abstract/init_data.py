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
    2. globalfeatures - gflen*byte
    3. flen - u16
    4. features - flen *byte
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
            length = len(self.raw[4 : 4 + (self.gflen.val*2)])
            if length% 4 != 0:
                tmp = '0' * abs(4-length) + self.raw[4 : 4+(self.gflen.val*2)]
            else:
                tmp = self.raw[4 : 4 + (self.gflen.val*2)]
            self.globalFeatures = bigsizeInt(tmp)
            self.globalFeatures.decode()
        flenStart = 4 + (self.gflen.val * 2)
        flenEnd = (self.gflen.val * 2) + 8
        self.flen = u16Int(self.raw[flenStart:flenEnd])
        self.flen.decode()
        if self.raw[flenEnd : flenEnd + self.flen.val]:
            length = len(self.raw[flenEnd : flenEnd + (self.flen.val*2)])
            if length% 4 != 0:
                tmp = '0' * (length%4) + self.raw[flenEnd : flenEnd + (self.flen.val*2)]
            else:
                tmp = self.raw[flenEnd : flenEnd + (self.flen.val*2)]
            self.features = bigsizeInt(tmp)
            self.features.decode()
        self.tvl_stream = TVLRecord(self.raw[flenEnd + self.flen.val * 2 :])
        self.tvl_stream.decode()

    def encode(self):
        if self.gflen.val > 0:
            self.globalFeatures.encode()
            assert len(self.globalFeatures.val) == self.gflen.val
            self.globalFeatures.val = str(self.globalFeatures.val.hex())[-self.gflen.val*2:]
        else:
            self.globalFeatures.val = ''
        if self.flen.val > 0:
            self.features.encode()
            assert len(self.features.val) == self.flen.val
            self.features.val = str(self.features.val.hex())[-self.flen.val*2:]
        else:
            self.features.val = ''
        self.tvl_stream.encode()
        self.gflen.encode()
        self.flen.encode()
        assert len(self.gflen.val) == 2
        assert len(self.flen.val) == 2
        self.encoded = str(self.gflen.val.hex()) + self.globalFeatures.val + str(self.flen.val.hex()) + self.features.val + self.tvl_stream.encoded


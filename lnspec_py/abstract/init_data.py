from ..fundamental.ints import u16Int
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

    def decode(self):
        self.gflen = u16Int(self.raw[:4])
        self.gflen.decode()
        if self.raw[4 : 4 + self.gflen.val]:
            self.globalFeatures = u16Int(self.raw[4 : 4 + self.gflen.val])
            self.globalFeatures.decode()
        flenStart = self.gflen.val
        flenEnd = self.gflen.val + 4 * 2
        self.flen = u16Int(self.raw[flenStart:flenEnd])
        self.flen.decode()
        self.features = u16Int(self.raw[flenEnd : flenEnd + self.flen.val * 2])
        self.features.decode()
        self.tvl_stream = TVLRecord(self.raw[flenEnd + self.flen.val * 2 :])
        self.tvl_stream.decode()

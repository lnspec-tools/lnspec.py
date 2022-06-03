from curses import raw
from ..FundamentalTypes.Integers import u16Integer, bigsize
import tlvRecord

class Init_data():
    def __init__(self, raw) -> None:
        self.raw = raw
    
    def decode(self):
        self.gflen = u16Integer(self.raw[:4])
        self.gflen.decode()
        self.globalFeatures = u16Integer(self.raw[4:int(self.gflen, 16)])
        self.globalFeatures.decode()
        flenStart = int(self.gflen, 16)
        flenEnd = int(self.gflen, 16)+4 *2
        self.flen = u16Integer(self.raw[flenStart:flenEnd])
        self.flen.decode()
        self.features = u16Integer(self.raw[flenEnd:  flenEnd + self.flen.val * 2])
        self.features.decode()
        self.tvl_stream = tlvRecord.TLV_record(self.raw[flenEnd + self.flen.val * 2:])
        self.tvl_stream.decode2()
        


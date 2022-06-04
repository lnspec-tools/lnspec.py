from ..fundamental.ints import u16Int
from .tlvRecord import TLVRecord

class InitMsg():
    def __init__(self, raw) -> None:
        self.raw = raw
    
    def decode(self):
        self.gflen = u16Int(self.raw[:4])
        self.gflen.decode()
        self.globalFeatures = u16Int(self.raw[4:int(self.gflen, 16)])
        self.globalFeatures.decode()
        flenStart = int(self.gflen, 16)
        flenEnd = int(self.gflen, 16)+4 *2
        self.flen = u16Int(self.raw[flenStart:flenEnd])
        self.flen.decode()
        self.features = u16Int(self.raw[flenEnd:  flenEnd + self.flen.val * 2])
        self.features.decode()
        self.tvl_stream = TLVRecord(self.raw[flenEnd + self.flen.val * 2:])
        self.tvl_stream.decode2()
        


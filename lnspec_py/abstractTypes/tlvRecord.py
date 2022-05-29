from curses import raw
from ..FundamentalTypes.Integers import bigsize

class TLV_record():
    def __init__(self, raw) -> None:
        self.raw = raw
        self.type = None
        self.length = None
        self.value = None
        self.decoded = None
    
    def decode(self):
        assert self.raw[:4] == '0208'
        assert self.raw[20:24] == '0304'
        if len(self.raw) > 32:
            assert self.raw[32:36] == '0404'
        self.raw = self.raw[4:20] + self.raw[24:32] + (self.raw[36:] if len(self.raw) > 34 else self.raw[32:])
        print(self.raw)
        if type(self.raw) == bytes:
            self.raw = self.raw.hex()    
        binary = bytes.fromhex(self.raw)
        _type = bigsize(binary[:8])
        length = bigsize(binary[8:12])
        _type.decode()
        length.decode()
        self.type = _type.val
        self.length = length.val
        self.value = binary[12: self.length]
        self.decoded = str(self.type) + ' ' + str(self.length) + ' ' + str(self.value.hex())
        print(self.decoded)

    def encode(self):
        pass



# 00023fff0003ffffff init message eg
class HexType():
    def __init__(self, val, size=32):
        self.size = size
        assert len(bytes.fromhex(val)) == size
        self.val = val
    
    def encode(self):
        self.val = bytes.fromhex(self.val)
        
    def decode(self):
        self.val = self.val.hex()


class ChainHash(HexType):
    pass

class channel_id(HexType):
    pass

class sha256(HexType):
    pass

class signature(HexType):
    def __init__(self, val, size=64):
        super().__init__(val, size)

class point(HexType):
    def __init__(self, val, size=33):
        super().__init__(val, size)

class short_channel_id(HexType):
    def __init__(self, val, size=8):
        super().__init__(val, size)
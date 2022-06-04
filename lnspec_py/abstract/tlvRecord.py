from curses import raw
from ..fundamental.ints import bigsizeInt

class TLVRecord():
    def __init__(self, raw) -> None:
        self.raw = raw
        self.types = []
        self.lengths = []
        self.values = []
        self.decodeds = []

    def decode(self):
        n = 0
        while n < len(self.raw):
            self.types.append(self.raw[n:n+2])
            n+=2
            length = self.raw[n:n+2]
            self.lengths.append(length)
            n+=2 
            if int(length, 16) == 0:
                raise Exception("Short read") 
            if n + int(length, 16) * 2 - 1 >= len(self.raw):
                raise Exception("out of range") 
            self.values.append('0x' + str(bytes.fromhex(self.raw[n:n+int(length, 16)*2]).hex()))
            n+= int(length, 16)*2


    def encode(self):
        pass



# 00023fff0003ffffff init message eg
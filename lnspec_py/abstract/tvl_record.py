from curses import raw
from ..fundamental.ints import bigsizeInt

"""
This class represent a single TVL record 
as specify in https://github.com/lightning/bolts/blob/master/01-messaging.md#type-length-value-format
"""


class TVLRecord:
    def __init__(self, raw) -> None:
        self.raw = raw
        self.types = []
        self.lengths = []
        self.values = []
        self.decodeds = []

    def decode(self):
        n = 0
        while n < len(self.raw):
            self.types.append(self.raw[n : n + 2])
            n += 2
            length = self.raw[n : n + 2]
            self.lengths.append(length)
            n += 2
            if int(length, 16) == 0:
                raise Exception("Short read")
            if n + int(length, 16) * 2 - 1 >= len(self.raw):
                raise Exception("out of range")
            self.values.append(
                "0x" + str(bytes.fromhex(self.raw[n : n + int(length, 16) * 2]).hex())
            )
            n += int(length, 16) * 2

    def encode(self):
        res = ''
        for x in range(len(self.types)):
            res += str(bytes.fromhex(self.types[x]).hex()) + str(bytes.fromhex(self.lengths[x]).hex()) + str(bytes.fromhex(self.value[x]).hex())
        self.encoded = res

# 00023fff0003ffffff init message eg

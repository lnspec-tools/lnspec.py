from abc import ABC, abstractmethod
import io

class Integer(ABC):
    @abstractmethod
    def encode(self):
        pass
    def decode(self):
        pass

class u16Integer(Integer):
    def __init__(self, val):
        self.val = val
    
    def encode(self):
        self.val = int.to_bytes(self.val,2,"big")

    def decode(self):
        self.val = int.from_bytes(self.val, "big")

class u32Integer(Integer):
    def __init__(self, val):
        self.val = val
    
    def encode(self):
        self.val = int.to_bytes(self.val,4,"big")

    def decode(self):
        self.val = int.from_bytes(self.val, "big")

class u64Integer(Integer):
    def __init__(self, val):
        self.val = val
    
    def encode(self):
        self.val = int.to_bytes(self.val,8,"big")

    def decode(self):
        self.val = int.from_bytes(self.val, "big")

class tu(Integer):
    def __init__(self, val):
        self.uintRange = [255, 65535, 16777215, 4294967295, 1099511627775, 281474976710655, 72057594037927935, 18446744073709551615]
        self.val = val
    
    def encode(self):
        for i in range(len(self.uintRange)):
            if self.val <= self.uintRange[i]:
                self.val = int.to_bytes(self.val,i+1, "big")
                break

    def decode(self):
        self.val = int.from_bytes(self.val, "big")

class bigsize(Integer):
    def __init__(self, val):
        self.val = val

    def decode(self):
        binary = bytes.fromhex(self.val)
        if (len(binary) == 3 and int.from_bytes(binary[1:],"big") < 0xFD) or (len(binary) == 5 and int.from_bytes(binary[1:],"big") <= 0xFFFF) or (len(binary) == 9 and int.from_bytes(binary[1:],"big") <= 0xFFFFFFFF):
            self.val = 'decoded bigsize is not canonical'
            return
        if len(binary) not in [1, 3, 5, 9]:
            self.val = "unexpected EOF"
            return
        _type = binary[0]
        if _type < 0xFD:
            self.val = int.from_bytes(binary, 'big')
        elif _type == 0xFD:
            self.val = int.from_bytes(binary[1:3], 'big')
        elif _type == 0xFE:
            self.val = int.from_bytes(binary[1:5], 'big')
        elif _type == 0xFF:
            self.val = int.from_bytes(binary[1:9], 'big')

    def encode(self):
        if self.val < 0xfd:
            size = 1
            _type = None
        elif self.val < 0x10000:
            size = 2
            _type = 0xfd
        elif self.val < 0x100000000:
            size = 4
            _type = 0xfe
        else:
            size = 8
            _type = 0xff
        self.val = int.to_bytes(self.val, size, "big")
        if _type:
            self.val = int.to_bytes(_type, 1, "big") + self.val[0:]


   
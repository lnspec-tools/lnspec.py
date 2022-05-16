from abc import ABC, abstractmethod

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

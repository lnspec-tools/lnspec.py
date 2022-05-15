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

class tu16(Integer):
    def __init__(self, val):
        self.val = val
    
    def encode(self):
        if self.val <= 255:
            self.val = int.to_bytes(self.val,1, "big")
        else:    
            self.val = int.to_bytes(self.val,2, "big")

    def decode(self):
        self.val = int.from_bytes(self.val, "big")


class tu32(Integer):
    def __init__(self, val):
        self.val = val
    
    def encode(self):
        if self.val <= 255:
            self.val = int.to_bytes(self.val,1, "big")
        elif self.val <= 65535:    
            self.val = int.to_bytes(self.val,2, "big")
        elif self.val <= 16777215:
            self.val = int.to_bytes(self.val,3, "big")

    def decode(self):
        self.val = int.from_bytes(self.val, "big")


class tu64(Integer):
    def __init__(self, val):
        self.val = val
    
    def encode(self):
        if self.val <= 255:
            self.val = int.to_bytes(self.val,1, "big")
        else:    
            self.val = int.to_bytes(self.val,2, "big")

    def decode(self):
        self.val = int.from_bytes(self.val, "big")
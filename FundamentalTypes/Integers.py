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
        self.val = bytes(self.val)

    def decode(self):
        self.val = int.from_bytes(self.val, "big")

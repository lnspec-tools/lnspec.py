from abc import ABC, abstractmethod

class message(ABC):
    @abstractmethod
    def encode(self):
        pass
    def decode(self):
        pass
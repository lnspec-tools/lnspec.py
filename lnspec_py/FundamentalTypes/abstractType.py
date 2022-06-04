from abc import ABC, abstractmethod


class HexType(ABC):
    @abstractmethod
    def encode(self):
        pass

    def decode(self):
        pass

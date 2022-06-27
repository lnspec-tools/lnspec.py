from abc import ABC, abstractmethod


class Message(ABC):
    @abstractmethod
    def encode(self):
        pass

    @classmethod
    def decode(raw_msg: str):
        pass

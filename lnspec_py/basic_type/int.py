from abc import ABC, abstractmethod
from typing import Tuple


"""
This module contain all the fundamental Ints types
as specify in https://github.com/lightning/bolts/blob/master/01-messaging.md#fundamental-types
"""


class Integer(ABC):
    @abstractmethod
    def encode(self):
        pass

    def decode(self):
        pass


class U16Int(Integer):
    def __init__(self, val: int) -> None:
        self.val = val

    def encode(self) -> str:
        self.val = int.to_bytes(self.val, 2, "big")
        return self.val.hex()

    def decode(self) -> "U16Int":
        if isinstance(self.val, str):
            self.val = bytes.fromhex(self.val)
        self.val = int.from_bytes(self.val, "big")
        return self

    @staticmethod
    def decode_with_hex_str(hex_str: str) -> Tuple["U16Int", str]:
        val = U16Int(hex_str[:4])
        hex_str = hex_str[4:]
        val.decode()
        return val, hex_str


class U32Int(Integer):
    def __init__(self, val):
        self.val = val

    def encode(self) -> str:
        self.val = int.to_bytes(self.val, 4, "big")
        return self.val.hex()

    def decode(self):
        if isinstance(self.val, str):
            self.val = bytes.fromhex(self.val)
        self.val = int.from_bytes(self.val, "big")

    @staticmethod
    def decode_with_hex_str(hex_str: str) -> Tuple["U32Int", str]:
        val = U32Int(hex_str[:8])
        hex_str = hex_str[8:]
        val.decode()
        return val, hex_str


class U64Int(Integer):
    def __init__(self, val):
        self.val = val

    def encode(self) -> str:
        self.val = int.to_bytes(self.val, 8, "big")
        return self.val.hex()

    def decode(self):
        self.val = int.from_bytes(self.val, "big")

    @staticmethod
    def decode_with_hex_str(hex_str: str) -> Tuple["U64Int", str]:
        val = U16Int(hex_str[:16])
        hex_str = hex_str[16:]
        val.decode()
        return val, hex_str


class tuInt(Integer):
    def __init__(self, val):
        self.uintRange = [
            255,
            65535,
            16777215,
            4294967295,
            1099511627775,
            281474976710655,
            72057594037927935,
            18446744073709551615,
        ]
        self.val = val

    def encode(self):
        for i in range(len(self.uintRange)):
            if self.val <= self.uintRange[i]:
                self.val = int.to_bytes(self.val, i + 1, "big")
                break

    def decode(self):
        self.val = int.from_bytes(self.val, "big")


class bigsizeInt(Integer):
    def __init__(self, val):
        self.val = val

    def decode(self):
        if isinstance(self.val, bytes):
            self.val = self.val.hex()
        binary = bytes.fromhex(self.val)
        if (
            (len(binary) == 3 and int.from_bytes(binary[1:], "big") < 0xFD)
            or (len(binary) == 5 and int.from_bytes(binary[1:], "big") <= 0xFFFF)
            or (len(binary) == 9 and int.from_bytes(binary[1:], "big") <= 0xFFFFFFFF)
        ):
            self.val = 0
            raise ValueError("decoded bigsize is not canonical")
        if len(binary) == 0:
            self.val = 0
            raise ValueError("unexpected EOF")
        _type = binary[0]
        if _type < 0xFD:
            self.val = int.from_bytes(binary, "big")
        elif _type == 0xFD:
            if len(binary) != 3:
                self.val = 0
                raise ValueError("unexpected EOF")
            self.val = int.from_bytes(binary[1:3], "big")
        elif _type == 0xFE:
            if len(binary) != 5:
                self.val = 0
                raise ValueError("unexpected EOF")
            self.val = int.from_bytes(binary[1:5], "big")
        elif _type == 0xFF:
            if len(binary) != 9:
                self.val = 0
                raise ValueError("unexpected EOF")
            self.val = int.from_bytes(binary[1:9], "big")

    def encode(self):
        if self.val < 0xFD:
            size = 1
            _type = None
        elif self.val < 0x10000:
            size = 2
            _type = 0xFD
        elif self.val < 0x100000000:
            size = 4
            _type = 0xFE
        else:
            size = 8
            _type = 0xFF
        self.val = int.to_bytes(self.val, size, "big")
        if _type:
            self.val = int.to_bytes(_type, 1, "big") + self.val[0:]

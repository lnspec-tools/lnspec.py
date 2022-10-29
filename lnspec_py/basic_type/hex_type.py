from typing import Tuple


class HexType:
    def __init__(self, val, size=32):
        self.size = size
        assert len(bytes.fromhex(val)) == size
        self.val = val

    def encode(self):
        self.val = bytes.fromhex(self.val)

    def decode(self):
        self.val = self.val.hex()


class ChainHash(HexType):
    pass


class ChannelId(HexType):
    def encode(self) -> str:
        self.val.encode()
        return self.val

    @staticmethod
    def decode_with_hex_str(hex_str: str) -> Tuple["ChannelId", str]:
        hex_str = hex_str[: (32 * 2)]
        val = ChannelId(hex_str)
        val.decode()
        return val, hex_str


class sha256(HexType):
    pass


class signature(HexType):
    def __init__(self, val, size=64):
        super().__init__(val, size)


class point(HexType):
    def __init__(self, val, size=33):
        super().__init__(val, size)


class short_channel_id(HexType):
    def __init__(self, val, size=8):
        super().__init__(val, size)

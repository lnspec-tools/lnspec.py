from typing import Tuple


class HexType:
    def __init__(self, val, size=32):
        self.size = size
        assert len(bytes.fromhex(val)) == size
        self.val = val

    def encode(self):
        self.val = bytes.fromhex(self.val)

    def decode(self):
        pass


class ChainHash(HexType):
    pass


class ChannelId(HexType):
    def encode(self) -> str:
        self.val.encode()
        # Source https://stackoverflow.com/a/27023448/10854225
        return self.val

    @staticmethod
    def decode_from_hex(hex_str: str) -> Tuple["ChannelId", str]:
        return ChannelId.decode_with_hex_str(hex_str)

    @staticmethod
    def decode_with_hex_str(hex_str: str) -> Tuple["ChannelId", str]:
        buff = hex_str[: (32 * 2)]
        val = ChannelId(buff)
        val.decode()
        hex_str = hex_str[(32 * 2) :]
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

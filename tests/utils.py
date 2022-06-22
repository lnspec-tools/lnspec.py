"""
Utils file that contains a sequence of useful code
to implement the integration testing for the serialization
and deserialization of the messages
"""
import io
from typing import Union, List
from pyln.proto.message import Message, MessageNamespace


class LNMessage:
    """
    LNMessage is an abstraction of the lnmessage
    taken from lnprototest https://github.com/rustyrussell/lnprototest
    """

    def __init__(self, type_name: str, csv: List, **kwargs: Union[str, int]):
        self.ns = MessageNamespace()
        self.ns.load_csv(csv)
        self.msg_typ = self.ns.get_msgtype(type_name)
        self.args = kwargs

    def resolve_arg(self, fieldname: str, arg):
        """If this is a string, return it, otherwise call it to get result
        taken from lnprototest https://github.com/rustyrussell/lnprototest
        """
        if callable(arg):
            return arg(self, fieldname)
        else:
            return arg

    def resolve_args(self, kwargs):
        """Take a dict of args, replace callables with their return values
        taken from lnprototest https://github.com/rustyrussell/lnprototest
        """
        ret = {}
        for field, str_or_func in kwargs.items():
            ret[field] = self.resolve_arg(field, str_or_func)
        return ret

    def encode(self) -> bytes:
        message = Message(self.msg_typ, **self.args)
        missing = message.missing_fields()
        if missing:
            raise Exception(f"Missing field {missing}")
        bin_msg = io.BytesIO()
        message.write(bin_msg)
        return bin_msg.getvalue()

    @staticmethod
    def decode(byte_string: bytes) -> "LNMessage":
        raise Exception("Not implemented yet")


def bitfield_len(bitfield: Union[List[int], str]) -> int:
    """Return length of this field in bits (assuming it's a bitfield!)

    taken from lnprototest https://github.com/rustyrussell/lnprototest"""
    if isinstance(bitfield, str):
        return len(bytes.fromhex(bitfield)) * 8
    else:
        return len(bitfield) * 8


def has_bit(bitfield: Union[List[int], str], bitnum: int) -> bool:
    """Test bit in this bitfield (little-endian, as per BOLTs)

    taken from lnprototest https://github.com/rustyrussell/lnprototest"""
    bitlen = bitfield_len(bitfield)
    if bitnum >= bitlen:
        return False

    # internal to a msg, it's a list of int.
    if isinstance(bitfield, str):
        byte = bytes.fromhex(bitfield)[bitlen // 8 - 1 - bitnum // 8]
    else:
        byte = bitfield[bitlen // 8 - 1 - bitnum // 8]

    if (byte & (1 << (bitnum % 8))) != 0:
        return True
    else:
        return False


def bitfield(*args: int) -> str:
    """Create a bitfield hex value with these bit numbers set
    taken from lnprototest https://github.com/rustyrussell/lnprototest"""
    bytelen = (max(args) + 8) // 8
    bfield = bytearray(bytelen)
    for bitnum in args:
        bfield[bytelen - 1 - bitnum // 8] |= 1 << (bitnum % 8)
    return bfield.hex()

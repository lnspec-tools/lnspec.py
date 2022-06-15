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
        """If this is a string, return it, otherwise call it to get result"""
        if callable(arg):
            return arg(self, fieldname)
        else:
            return arg

    def resolve_args(self, kwargs):
        """Take a dict of args, replace callables with their return values"""
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

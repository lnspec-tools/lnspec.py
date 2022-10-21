#!/usr/bin/env python3
from lnspec_py.message_type.bolt1 import InitMsg
from .utils import LNMessage
from pyln.spec.bolt1 import bolt


def test_simple_init_message():
    msg = LNMessage(
        "init",
        csv=bolt.csv,
        globalfeatures="",
        features="",
    )
    assert str(msg.encode().hex()) == msg.encode().hex()
    init_msg = InitMsg.decode(raw_msg=msg.encode().hex())
    # type message with value 16 is the init message
    assert init_msg.encode() == msg.encode().hex()

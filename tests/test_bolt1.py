#!/usr/bin/env python3
from lnspec_py.message_type.bolt1 import InitMsg, ErrorMsg
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


def test_simple_error_message():
    msg = LNMessage(
        "error",
        csv=bolt.csv,
        channel_id="399986f8d47b36d4f21c07de0ce7d422de244ed58a72e6b44d26985fe1e7465c",
        data="0003",
    )

    assert str(msg.encode().hex()) == msg.encode().hex()
    init_msg = ErrorMsg.decode(raw_msg=msg.encode().hex())
    # type message with value 16 is the init message
    assert init_msg.encode() == msg.encode().hex()

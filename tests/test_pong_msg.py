from black import err
import pytest
from lnspec_py.message_type.ping_pong import PongMessage
from .utils import LNMessage
from pyln.spec.bolt1 import bolt


def test_simple_good_case():
    a = PongMessage.decode("001300080000000000000000")
    assert a.msg_type.val == 19
    assert a.bytesLen.val == 8
    assert len(a.ignored) == 0

    assert a.encode() == "001300080000000000000000"


def test_simple_pong_message():
    msg = LNMessage(
        "pong",
        csv=bolt.csv,
        ignored=[1],
    )
    assert str(msg.encode().hex()) == msg.encode().hex()
    pong_msg = PongMessage.decode(raw_msg=msg.encode().hex())
    assert pong_msg.msg_type.val == 19
    assert pong_msg.bytesLen.val == 1
    assert pong_msg.ignored == [0]
    assert pong_msg.encode() == msg.encode().hex()

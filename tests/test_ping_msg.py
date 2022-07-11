from black import err
import pytest
from lnspec_py.message_type.ping_pong import PingMessage
from .utils import LNMessage

from pyln.spec.bolt1 import bolt


def test_simple_good_case():
    a = PingMessage.decode("0012fffb00080000000000000000")
    assert a.msg_type.val == 18
    assert a.numPongBytes.val == 65531
    assert a.bytesLen.val == 8
    assert len(a.ignored) == 0

    assert a.encode() == "0012fffb00080000000000000000"


def test_simple_ping_message():
    msg = LNMessage("ping", csv=bolt.csv, ignored=[2], num_pong_bytes=65531)
    assert str(msg.encode().hex()) == msg.encode().hex()
    ping_msg = PingMessage.decode(raw_msg=msg.encode().hex())
    assert ping_msg.msg_type.val == 18
    assert ping_msg.bytesLen.val == 1
    assert ping_msg.ignored == [1]
    assert ping_msg.numPongBytes.val == 65531
    assert ping_msg.encode() == msg.encode().hex()

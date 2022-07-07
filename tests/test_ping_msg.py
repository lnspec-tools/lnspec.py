from black import err
import pytest
from lnspec_py.message_type.ping_pong import PingMessage


def test_simple_good_case():
    a = PingMessage.decode("0012fffb00080000000000000000")
    assert a.msg_type.val == 18
    assert a.numPongBytes.val == 65531
    assert a.bytesLen.val == 8
    assert len(a.ignored) == 0

    assert a.encode() == "0012fffb00080000000000000000"

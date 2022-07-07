from black import err
import pytest
from lnspec_py.message_type.ping_pong import PongMessage


def test_simple_good_case():
    a = PongMessage.decode("001300080000000000000000")
    assert a.msg_type.val == 19
    assert a.bytesLen.val == 8
    assert len(a.ignored) == 0

    assert a.encode() == "001300080000000000000000"

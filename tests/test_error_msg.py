from black import err
import pytest
from lnspec_py.message_type.error import ErrorMessage
from .utils import LNMessage

from pyln.spec.bolt1 import bolt


def test_simple_good_case():
    a = ErrorMessage.decode(
        "0011399986f8d47b36d4f21c07de0ce7d422de244ed58a72e6b44d26985fe1e7465c000102"
    )
    assert (
        a.channel_id.val
        == "399986f8d47b36d4f21c07de0ce7d422de244ed58a72e6b44d26985fe1e7465c"
    )
    assert a.len.val == 1
    assert a.data[0] == 1

    assert (
        a.encode()
        == "0011399986f8d47b36d4f21c07de0ce7d422de244ed58a72e6b44d26985fe1e7465c000102"
    )


def test_simple_error_message():
    msg = LNMessage(
        "error",
        csv=bolt.csv,
        channel_id="399986f8d47b36d4f21c07de0ce7d422de244ed58a72e6b44d26985fe1e7465c",
        data="0003",
    )
    assert str(msg.encode().hex()) == msg.encode().hex()
    error_msg = ErrorMessage.decode(raw_msg=msg.encode().hex())
    assert error_msg.msg_type.val == 17
    assert error_msg.encode() == msg.encode().hex()

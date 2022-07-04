from black import err
import pytest
from lnspec_py.message_type.error import ErrorMessage


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

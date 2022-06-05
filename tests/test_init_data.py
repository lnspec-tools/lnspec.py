import sys
import path
import pytest

directory = path.Path(__file__).abspath()
# setting path
sys.path.append(directory.parent.parent)
from lnspec_py.messagesTypes.InitMsg import InitMessage


def test_simple_good_case():
    a = InitMessage("001000000000c9012acb0104")
    a.decode()
    assert a.type.val == 16
    assert 'c9' in a.data.tvl_stream.types
    assert 'cb' in a.data.tvl_stream.types


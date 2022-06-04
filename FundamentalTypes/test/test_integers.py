import sys
import path

directory = path.path(__file__).abspath()
# setting path
sys.path.append(directory.parent.parent)
from FundamentalTypes.Integers import u16Integer
import pytest


def test_u16Integer():
    a = u16Integer(16)
    a.encode()
    print(a.val)
    assert a.val == 0


test_u16Integer()

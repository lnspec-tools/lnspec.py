import sys
import path
import pytest

directory = path.Path(__file__).abspath()
# setting path
sys.path.append(directory.parent.parent)
from lnspec_py.abstractTypes.tlvRecord import TLV_record


def test_simple_good_case():
    a = TLV_record("0208deadbeef1badbeef03041bad1dea")
    a.decode()
    assert int(str(a.type)) == int("0xdeadbeef1badbeef", 16)
    assert int(str(a.length)) == int("0x1bad1dea", 16)
    assert a.value == b""
    b = TLV_record("0208deadbeef1badbeef03041bad1dea040401020304")
    b.decode()
    assert int(str(b.type)) == int("0xdeadbeef1badbeef", 16)
    assert int(str(b.length)) == int("0x1bad1dea", 16)
    assert b.value.hex() in "0x01020304"


def test_short_read():
    a = TLV_record("01000208deadbeef1badbeef0308deadbeef")
    with pytest.raises(AssertionError) as info:
        a.decode()


def test_types_out_of_order():
    tests = [
        "01000304deadbeef0208deadbeef1badbeef",
        "0208deadbeef1badbeef01000304deadbeef",
    ]
    for x in tests:
        a = TLV_record(x)
        with pytest.raises(AssertionError) as info:
            a.decode()


def test_req_type_missing_or_extra():
    tests = [
        "01000208deadbeef1badbeef0304deadbeef0600",
        "01000208deadbeef1badbeef",
        "0304deadbeef0500",
    ]
    for x in tests:
        a = TLV_record(x)
        with pytest.raises(AssertionError) as info:
            a.decode()

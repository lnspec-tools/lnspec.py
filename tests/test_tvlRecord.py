import pytest

from lnspec_py.abstract.tvl_Record import TVLRecord

"""
Test for TVL reader
1. Pass raw message into TVLRecord Object
2. Call decode
3. Compare result types, lenghts with expected values
"""

def test_simple_good_case():
    a = TVLRecord("0208deadbeef1badbeef03041bad1dea")
    a.decode()
    expected = [["02", "08", "0xdeadbeef1badbeef"], ["03", "04", "0x1bad1dea"]]
    for x in expected:
        assert x[0] in [str(i) for i in a.types]
        assert x[1] in [str(i) for i in a.lengths]
        assert x[2] in a.values
    b = TVLRecord("0208deadbeef1badbeef03041bad1dea040401020304")
    b.decode()
    expected = [["02", "08", "0xdeadbeef1badbeef"], ["03", "04", "0x1bad1dea"]]
    for x in expected:
        assert x[0] in [str(i) for i in b.types]
        assert x[1] in [str(i) for i in b.lengths]
        assert x[2] in b.values


def test_short_read():
    a = TVLRecord("01000208deadbeef1badbeef0308deadbeef")
    with pytest.raises(Exception) as info:
        a.decode()


def test_types_out_of_order():
    tests = [
        "01000304deadbeef0208deadbeef1badbeef",
        "0208deadbeef1badbeef01000304deadbeef",
    ]
    for x in tests:
        a = TVLRecord(x)
        with pytest.raises(Exception) as info:
            a.decode()


def test_req_type_missing_or_extra():
    tests = [
        "01000208deadbeef1badbeef0304deadbeef0600",
        "01000208deadbeef1badbeef",
        "0304deadbeef0500",
    ]
    for x in tests:
        a = TVLRecord(x)
        with pytest.raises(Exception) as info:
            a.decode()


def test_decode2():
    a = TVLRecord("0208deadbeef1badbeef03041bad1dea")
    a.decode()
    expected = [["02", "08", "0xdeadbeef1badbeef"], ["03", "04", "0x1bad1dea"]]
    for x in expected:
        assert x[0] in [str(i) for i in a.types]
        assert x[1] in [str(i) for i in a.lengths]
        assert x[2] in a.values

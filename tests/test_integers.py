import sys
import pytest
import lnspec_py.FundamentalTypes.Integers as Integers


def test_u16Integer():
    a = Integers.u16Integer(16)
    a.encode()
    assert a.val.hex() == "0010"
    a.decode()
    assert a.val == 16


def test_u32Integer():
    a = Integers.u32Integer(4294967295)
    a.encode()
    assert a.val.hex() == "ffffffff"
    a.decode()
    assert a.val == 4294967295


def test_u64Integer():
    a = Integers.u64Integer(18446744073709551615)
    a.encode()
    assert a.val.hex() == "ffffffffffffffff"
    a.decode()
    assert a.val == 18446744073709551615


def test_tuInteger():
    a = Integers.tu(0)
    vals = a.uintRange
    for i in range(len(vals)):
        a = Integers.tu(vals[i])
        a.encode()
        assert a.val.hex() == "f" * len(a.val.hex())
        a.decode()
        assert a.val == vals[i]


def test_bigsize():
    decoded_tests = [
        "00",
        "fc",
        "fd00fd",
        "fdffff",
        "fe00010000",
        "feffffffff",
        "ff0000000100000000",
        "ffffffffffffffffff",
    ]
    expected_decoded = [
        0,
        252,
        253,
        65535,
        65536,
        4294967295,
        4294967296,
        18446744073709551615,
    ]
    for i in range(len(decoded_tests)):
        a = Integers.bigsize(decoded_tests[i])
        a.decode()
        print(a.val)
        assert a.val == expected_decoded[i]
        a.encode()
        assert a.val.hex() == decoded_tests[i]


def test_bigSize_ERROR():
    error_tests = [
        "fd00fc",
        "fe0000ffff",
        "ff00000000ffffffff",
        "fd00",
        "feffff",
        "ffffffffff",
        "",
        "fd",
        "fe",
        "ff",
    ]
    expected_errors = ["decoded bigsize is not canonical"] * 3 + ["unexpected EOF"] * 7
    for i in range(len(error_tests)):
        a = Integers.bigsize(error_tests[i])
        with pytest.raises(ValueError) as info:
            a.decode()
            assert expected_errors[i] in str(info)


def test_bigSize_encode():
    encode_tests = [
        0,
        252,
        253,
        65535,
        65536,
        4294967295,
        4294967296,
        18446744073709551615,
    ]
    expected_encode = [
        "00",
        "fc",
        "fd00fd",
        "fdffff",
        "fe00010000",
        "feffffffff",
        "ff0000000100000000",
        "ffffffffffffffffff",
    ]
    for i in range(len(encode_tests)):
        a = Integers.bigsize(encode_tests[i])
        a.encode()
        print(a.val)
        assert a.val.hex() == expected_encode[i]
        a.decode()
        assert a.val == encode_tests[i]

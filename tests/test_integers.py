import sys
import path

directory = path.Path(__file__).abspath()  
# setting path
sys.path.append(directory.parent.parent)
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
        assert a.val.hex() == 'f' * len(a.val.hex())
        a.decode()
        assert a.val == vals[i]


def test_bigsize():
    decoded_tests = ["00", "fc", "fd00fd", 'fdffff', 'fe00010000', 'feffffffff', 'ff0000000100000000', 'ffffffffffffffffff', 'fd00fc']
    expected_decoded = [0, 252, 253, 65535, 65536,4294967295, 4294967296, 18446744073709551615, "decoded bigsize is not canonical"]
    for i in range(len(decoded_tests)):
        a = Integers.bigsize(decoded_tests[i])
        a.decode()
        print(a.val)
        assert a.val == expected_decoded[i]
        if a.val != "decoded bigsize is not canonical":
            a.encode()
            assert a.val.hex() == decoded_tests[i]

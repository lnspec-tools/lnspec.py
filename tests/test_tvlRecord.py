import sys
import path
import pytest

directory = path.Path(__file__).abspath()  
# setting path
sys.path.append(directory.parent.parent)
from lnspec_py.abstract.tlvRecord import TLVRecord

def test_simple_good_case():
    a = TLVRecord("0208deadbeef1badbeef03041bad1dea")
    a.decode()
    expected = [['02', '08', "0xdeadbeef1badbeef"], ["03", "04", "0x1bad1dea"]]
    for x in expected:
        assert x[0] in [str(i) for i in a.types]
        assert x[1] in [str(i) for i in a.lengths]
        assert x[2] in a.values
    b = TLVRecord("0208deadbeef1badbeef03041bad1dea040401020304")
    b.decode()
    expected = [['02', '08', "0xdeadbeef1badbeef"], ["03", "04", "0x1bad1dea"]]
    for x in expected:
        assert x[0] in [str(i) for i in b.types]
        assert x[1] in [str(i) for i in b.lengths]
        assert x[2] in b.values

def test_short_read():
    a = TLVRecord("01000208deadbeef1badbeef0308deadbeef")
    with pytest.raises(Exception) as info:
        a.decode()

def test_types_out_of_order():
    tests = ["01000304deadbeef0208deadbeef1badbeef", "0208deadbeef1badbeef01000304deadbeef"]
    for x in tests:
        a = TLVRecord(x)
        with pytest.raises(Exception) as info:
            a.decode()

def test_req_type_missing_or_extra():
    tests = ["01000208deadbeef1badbeef0304deadbeef0600", "01000208deadbeef1badbeef", "0304deadbeef0500"]
    for x in tests:
        a = TLVRecord(x)
        with pytest.raises(Exception) as info:
            a.decode()

def test_decode2():
    a = TLVRecord("0208deadbeef1badbeef03041bad1dea")
    a.decode()
    expected = [['02', '08', "0xdeadbeef1badbeef"], ["03", "04", "0x1bad1dea"]]
    for x in expected:
        assert x[0] in [str(i) for i in a.types]
        assert x[1] in [str(i) for i in a.lengths]
        assert x[2] in a.values

    
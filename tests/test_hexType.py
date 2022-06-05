import sys
import path

directory = path.Path(__file__).abspath()
# setting path
sys.path.append(directory.parent.parent)
import lnspec_py.fundamental.hexType as hexType


def test_u16Integer():
    a = hexType.ChainHash(
        "6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000"
    )
    a.encode()
    assert a.val != "6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000"
    a.decode()
    assert a.val == "6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000"

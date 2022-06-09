import lnspec_py.fundamental.hex_Type as hex_Type

"""
Test for Hex type

ChainHash: https://github.com/lightning/bolts/blob/master/00-introduction.md#glossary-and-terminology-guide
"""


def test_hexType():
    a = hex_Type.ChainHash(
        "6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000"
    )
    a.encode()
    assert a.val != "6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000"
    a.decode()
    assert a.val == "6fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000"

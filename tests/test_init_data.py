from lnspec_py.messagesTypes.Init_Msg import InitMessage
from .utils import LNMessage
from pyln.spec.bolt1 import bolt


def test_simple_good_case():
    a = InitMessage("001000000000c9012acb0104")
    a.decode()
    assert a.type.val == 16
    assert "c9" in a.data.tvl_stream.types
    assert "cb" in a.data.tvl_stream.types


def test_simple_init_message_integration_test():
    msg = LNMessage(
        "init",
        csv=bolt.csv,
        features=[1, 2, 3, 4, 5],
        globalfeatures=[9, 2, 1, 2, 3, 4, 5],
    )
    encode = InitMessage(str(msg.encode().hex()))
    print(str(msg.encode().hex()))
    encode.decode()
    # type message with value 16 is the init message
    assert encode.type.val == 16
    encode.encode()
    assert len(encode.encoded) == len(msg.encode().hex())
    assert encode.encoded == msg.encode().hex()

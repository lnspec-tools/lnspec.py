from lnspec_py.messagesTypes.init_msg import InitMessage
from .utils import LNMessage, bitfield
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
        globalfeatures="",
        features=bitfield(12, 20, 29),
    )
    assert str(msg.encode().hex()) == msg.encode().hex()
    init_msg = InitMessage(msg.encode().hex())
    init_msg.decode()
    # type message with value 16 is the init message
    assert init_msg.type.val == 16
    assert init_msg.data.globalFeatures == ""
    assert init_msg.data.features == bitfield(12, 20, 29)

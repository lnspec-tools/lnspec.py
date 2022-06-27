import logging

from lnspec_py.messages_types.init_msg import InitMessage
from lnspec_py.basic_type.bitmask import Bitfield
from .utils import LNMessage, bitfield
from pyln.spec.bolt1 import bolt


def test_simple_good_case():
    a = InitMessage.decode("001000000000c9012acb0104")
    assert a.type.val == 16
    assert "c9" in a.data.tvl_stream.types
    assert "cb" in a.data.tvl_stream.types


def test_simple_init_message_integration_test_simple():
    msg = LNMessage(
        "init",
        csv=bolt.csv,
        globalfeatures="",
        features="",
    )
    assert str(msg.encode().hex()) == msg.encode().hex()
    init_msg = InitMessage.decode(raw_msg=msg.encode().hex())
    # type message with value 16 is the init message
    assert init_msg.type.val == 16
    assert init_msg.data.global_features == []
    assert init_msg.data.features == []
    assert init_msg.encode() == msg.encode().hex()


def test_simple_init_message_integration_test_feature():
    msg = LNMessage(
        "init",
        csv=bolt.csv,
        globalfeatures="",
        features=bitfield(12, 20, 29),
    )
    assert str(msg.encode().hex()) == msg.encode().hex()
    init_msg = InitMessage.decode(raw_msg=msg.encode().hex())
    # type message with value 16 is the init message
    assert init_msg.type.val == 16
    assert init_msg.data.global_features == []
    init_msg.data.features.sort()
    assert init_msg.data.features == [12, 20, 29]
    assert Bitfield.encode(init_msg.data.features) == bitfield(12, 20, 29)
    assert init_msg.encode() == msg.encode().hex()


def test_simple_init_message_integration_test_global_feature():
    msg = LNMessage(
        "init",
        csv=bolt.csv,
        globalfeatures=bitfield(12, 20, 29),
        features="",
    )
    assert str(msg.encode().hex()) == msg.encode().hex()
    init_msg = InitMessage.decode(raw_msg=msg.encode().hex())

    # type message with value 16 is the init message
    assert init_msg.type.val == 16
    assert init_msg.data.features == []
    init_msg.data.global_features.sort()
    logging.debug(f"expected gloabl feature hex: {bitfield(12, 20, 29)}")
    assert init_msg.data.global_features == [12, 20, 29]
    assert Bitfield.encode(init_msg.data.global_features) == bitfield(12, 20, 29)
    assert init_msg.encode() == msg.encode().hex()

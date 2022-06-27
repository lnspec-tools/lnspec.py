from .utils import bitfield
from lnspec_py.basic_type.bitmask import Bitfield


def test_bitfiled_encoding():
    expected_bitfield = bitfield(7)
    encoded_bitfield = Bitfield.encode([7])
    assert expected_bitfield == encoded_bitfield


def test_bitfiled_decoding():
    expected_bitfield = [7]
    encoded_bitfield = Bitfield.encode([7])
    decoded_bitfield = Bitfield.decode(encoded_bitfield)
    assert expected_bitfield == decoded_bitfield


def test_bitfiled_encoding_complex():
    expected_bitfield = bitfield(7, 2, 4, 7)
    encoded_bitfield = Bitfield.encode([7, 2, 4, 7])
    assert expected_bitfield == encoded_bitfield


def test_bitfiled_decoding_complex():
    expected_bitfield = [7, 2, 4]
    encoded_bitfield = Bitfield.encode([7, 2, 4, 7])
    decoded_bitfield = Bitfield.decode(encoded_bitfield)
    expected_bitfield.sort()
    decoded_bitfield.sort()
    assert expected_bitfield == decoded_bitfield


def test_bitfield_decoding_from_hex():
    expected_bitfield = [7, 12]
    hex_bitfield = bitfield(7, 12)
    decoded_bitfield = Bitfield.decode(hex_str=hex_bitfield)
    assert expected_bitfield == decoded_bitfield

from typing import Union, List


def bitfield_len(bitfield: Union[List[int], str]) -> int:
    """Return length of this field in bits (assuming it's a bitfield!)"""
    if isinstance(bitfield, str):
        return len(bytes.fromhex(bitfield)) * 8
    else:
        return len(bitfield) * 8


def has_bit(bitfield: Union[List[int], str], bitnum: int) -> bool:
    """Test bit in this bitfield (little-endian, as per BOLTs)"""
    bitlen = bitfield_len(bitfield)
    if bitnum >= bitlen:
        return False

    # internal to a msg, it's a list of int.
    if isinstance(bitfield, str):
        byte = bytes.fromhex(bitfield)[bitlen // 8 - 1 - bitnum // 8]
    else:
        byte = bitfield[bitlen // 8 - 1 - bitnum // 8]

    if (byte & (1 << (bitnum % 8))) != 0:
        return True
    else:
        return False


def bitfield(*args: int) -> str:
    """Create a bitfield hex value with these bit numbers set"""
    bytelen = (max(args) + 8) // 8
    bfield = bytearray(bytelen)
    for bitnum in args:
        bfield[bytelen - 1 - bitnum // 8] |= 1 << (bitnum % 8)
    return bfield.hex()


def int_to_bitfield(n: int) -> list:
    a = [int(digit) for digit in bin(n)[2:]]
    if len(a) % 8 != 0:
        a = [0] * (8 - len(a) % 8) + a
    return a


def bitfield_to_int(n: list) -> int:
    # convert the index of set bits to integer
    # input should be something like this [2, 3] where 2 & 3 indicate index 2 & 3 is set to 1 == 1100
    # output is a integer
    # return sum (2**i) where i is the set index
    return sum([2**i for i in n])


def pad_zero_Hex(n: str) -> str:
    if len(n) % 2 != 0:
        return ("0" * (2 - (len(n) % 2))) + n
    return n


def remove_leading_zero(n: str) -> str:
    try:
        while n[0] == "0":
            n = n[1:]
        return n
    except:
        return n

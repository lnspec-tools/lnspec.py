"""
This file includes the definition of the bitmask definition and gives the possibility to encode and decode
 the array of value in and from hex

But before WHAT IS A BITFIELD?
 - an encoding of integer in as bitmask.

What is a bitmask?

From Stackoverflow (https://stackoverflow.com/a/31576303/10854225)

bitmask is: It is just a number, as represented in binary.
For example, let's say I have 8 boolean values (true or false)
that I want to store. I could store it as an array of 8 booleans, or I could store it as a single byte (8 bits),
each of which store one of the booleans (0 = false, 1 = true).

At this point, I can easily manipulate my byte so that I can (1) set specific bits to be on or off (true or false),
and (2) check whether specific bits are on or off.

To set a bit to 1: mask = mask | (1 << bitIndex)
To set a bit to 0: mask = mask & ~(1 << bitIndex)
To get a bit (to be able to check it): (mask & (1 << bitIndex)) != 0

All of these operations use the left-shift operator, which moves bits up from least-significant
to most-significant positions.

 author: https://github.com/vincenzopalazzo
"""
from typing import List


class Bitfield:
    """
    Bitfiles is a class that gives you the possibility to encode and decode
    a sequence of number (feature) in an array where these numbers are set to true.
    """

    @staticmethod
    def encode(feature: List[int]) -> str:
        assert len(feature) > 0
        max_length = (max(feature) + 8) // 8
        bitfield = bytearray(max_length)
        for feature in feature:
            # Set the bit to 1
            bitfield[max_length // 8 - 1 - feature // 8] |= 1 << (feature % 8)
        return bitfield.hex()

    @staticmethod
    def decode(hex_str: str) -> List[int]:
        bitfield = bytearray.fromhex(hex_str) * 8
        max_len = len(bitfield)
        feature = []
        for idx in range(0, max_len):
            # has filed
            if (bitfield[max_len // 8 - 1 - idx // 8] & (1 << idx)) != 0:
                feature.append(idx)
        return feature
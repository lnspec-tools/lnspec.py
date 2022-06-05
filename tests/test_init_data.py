import sys
import path
import pytest

directory = path.Path(__file__).abspath()
# setting path
sys.path.append(directory.parent.parent)
from lnspec_py.abstract.init_data import InitMsg


def test_simple_good_case():
    pass

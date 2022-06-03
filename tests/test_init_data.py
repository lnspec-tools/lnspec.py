import sys
import path
import pytest

directory = path.Path(__file__).abspath()  
# setting path
sys.path.append(directory.parent.parent)
from lnspec_py.abstractTypes.init_data import Init_data

def test_simple_good_case():
    pass
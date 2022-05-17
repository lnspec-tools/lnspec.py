from msg import message
from ..FundamentalTypes import Integers

class InitMessage(message):
    def __init__(self, _type : Integers.u16Integer, data : dict):
        self.type = _type
        self.gflen = data['gflen']
        self.globalfeatures = data['globalfeatures']
        self.flen = data['flen']
        self.features = data['features']
        self.init_tlvs = data['tlvs']
        
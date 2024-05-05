from GeneralObjects import AddressIPv4, AddressIPv6

class RIB_Class:
    def __init__(self, _level: int):
        self.prefixCounter: int = 0
        self.left = None
        self.right = None
        self.mask = _level
    
    def SetLeft(self, _level):
        if self.left == None:
            self.left = RIB_Class(_level)

    def SetRight(self, _level):
        if self.right == None:
            self.right = RIB_Class(_level)
    
    def SavePrefix(self, _address: AddressIPv4|AddressIPv6) -> bool:
        if self.mask == _address.mask:
            self.prefixCounter += 1
            if self.prefixCounter == 1:
                return True
            else:
                return False

        if _address.GetBitValue(self.mask) == 1:
            self.SetRight(self.mask + 1)
            return self.right.SavePrefix(_address)
        else:
            self.SetLeft(self.mask + 1)
            return self.left.SavePrefix(_address)

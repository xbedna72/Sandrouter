import json
from FIB_Models.BinaryTrie import BinaryTrie
from GeneralObjects import Address

class Base:
    def __init__(self, _level: int):
        self.prefixCounter: int = 0
        self.left = None
        self.right = None
        self.mask = _level
    
    def SetLeft(self, _level):
        if self.left == None:
            self.left = Base(_level)

    def SetRight(self, _level):
        if self.right == None:
            self.right = Base(_level)
    
    def SavePrefix(self, _address: Address) -> int:
        if self.mask == _address.mask:
            self.prefixCounter = self.prefixCounter + 1
            return self.prefixCounter

        if _address.GetBitValue(self.mask) == 1:
            self.SetRight(self.mask + 1)
            return self.right.SavePrefix(_address)
        else:
            self.SetLeft(self.mask + 1)
            return self.left.SavePrefix(_address)

def DeletePrefix(node: Base, _address: Address) -> bool:
    result = False
    if (node == None) or (node.mask > _address.mask):
        return result     #The address not in RIB

    if node.mask < _address.mask:
        if _address.GetBitValue(node.mask) == 0:
            result = DeletePrefix(node.right, _address)
            if result == True:
                del node.right
                node.right = None
        else:
            result = DeletePrefix(node.left, _address)
            if result == True:
                del node.left
                node.left = None
    
    if node.mask == _address.mask:
        if node.prefixCounter > 0:
            node.prefixCounter = node.prefixCounter - 1
        
    if node.prefixCounter == 0 and node.left == None and node.right == None:
        return True               #I am ready to be deleted
    
    return result

def GetArrayOfPrefixesOnLevel(_root:Base, _level:int, _list):
    if _root == None:
        return
    
    if _root.mask == _level:
        if _root.left == None and _root.right == None:
            _list.append([_root.prefixCounter, 0])
        elif _root.left != None and _root.right != None:
            _list.append([_root.prefixCounter, 2])
        else:
            _list.append([_root.prefixCounter, 1])
        return

    if _root.mask < _level:
        GetArrayOfPrefixesOnLevel(_root.left, _level, _list)
        GetArrayOfPrefixesOnLevel(_root.right, _level, _list)

def GenerateTables_ModelFIB(_file: str):
    print("Not Implemented")

def GenerateTables_BinarieTrieFIB(_file: str) -> tuple[Base, BinaryTrie]:
    RIB = Base(0)
    file = open(_file, 'r')
    lines = file.readlines()
    fib = BinaryTrie()

    for line in lines:
        if line != '\n':
            line2 = line.split('\n')
            addr = None
            addr = Address(line2[0])
            val = RIB.SavePrefix(addr)
            if val == 1:
                fib.SavePrefix(addr)
    return (RIB, fib)

def PutUpdates(_file: str, RIB: Base, FIB: BinaryTrie, updateAnalyser, overallAnalyser) -> Base:
    file = open(_file, 'r')
    lines = file.readlines()
    iter = 0

    for line in lines:
        address = line.split(' ')
        addr = Address(address[1])

        if address[0] == 'A':
            if RIB.SavePrefix(addr) == 1:
                action = FIB.SavePrefix(addr)
                #updateAnalyser.SaveAction(action)
        
        if address[0] == 'W':
            message = DeletePrefix(RIB, addr)
            if message:
                action = FIB.DeletePrefix(addr)
                #updateAnalyser.DeleteAction(action)
        iter += 1

        if iter == 5000:
            iter = 0
            overallAnalyser.AddStatData(FIB.GetStatistics())

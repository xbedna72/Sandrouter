from FIB.BinaryTrie import BinaryTrie
from FIB.TreeBitmap import TreeBitmap
from FIB.FIBModel import FIBModel
from GeneralObjects import AddressIPv4, AddressIPv6
from RIB import RIB_Class

def Find(root, _addr: AddressIPv4|AddressIPv6):        
    if root.mask == _addr.mask:
        return (True, root.prefixCounter)
    
    if _addr.GetBitValue(root.mask) == 1:
        if root.right != None:
            return Find(root.right, _addr)
        else:
            return (False, 0)
    else:
        if root.left != None:
            return Find(root.left, _addr)
        else:
            return (False, 0)


def DeletePrefix(node: RIB_Class, _address: AddressIPv4|AddressIPv6) -> tuple[bool, bool]:
    result = False
    ready = False
    if (node == None) or (node.mask > _address.mask):
        return (False, False)     #The address not in RIB

    if node.mask < _address.mask:
        if _address.GetBitValue(node.mask) == 1:
            result, ready = DeletePrefix(node.right, _address)
            if ready == True:
                node.right = None
        else:
            result, ready = DeletePrefix(node.left, _address)
            if ready == True:
                node.left = None
    
    if node.mask == _address.mask:
        if node.prefixCounter > 0:
            node.prefixCounter -= 1
        if node.prefixCounter == 0:
            result = True
    
    if node.left == None and node.right == None and node.prefixCounter == 0:
        ready = True               #I am ready to be deleted
    else:
        ready = False
    
    return (result, ready)

def GenerateTables(_file: str, _model: int, _type: str)->tuple[RIB_Class, TreeBitmap|BinaryTrie|FIBModel]:
    RIB = RIB_Class(0)
    file = open(_file, 'r')
    lines = file.readlines()
    fib = None

    if _model == 0:
        print("Binary Trie")
        fib = BinaryTrie()
    elif _model == 1:
        print("TreeBitmap")
        fib = TreeBitmap()
    else:
        print("FIBModel")
        fib = FIBModel()

    for line in lines:
        if line != '\n':
            line2 = line.split('\n')
            addr = None
            if _type == "ipv4":
                addr = AddressIPv4(line2[0])
            else:
                addr = AddressIPv6(line2[0])
                
            val = RIB.SavePrefix(addr)
            if val:
                fib.SavePrefix(addr)
    return (RIB, fib)

def PutUpdates(_file: str, RIB: RIB_Class, FIB:TreeBitmap|BinaryTrie|FIBModel, updateAnalyser, overallAnalyser, _iter: int, _type: str):
    print("Benchmark executed.")
    file = open(_file, 'r')
    lines = file.readlines()
    iter = 0
    updates = 0

    overallAnalyser.AddStatData(FIB.GetStatistics())

    updateAnalyser.levels = overallAnalyser.GetNumberOfNodesEachLevel()

    for line in lines:
        line2 = line.split('\n')
        address = line2[0].split(' ')
        addr = None
        updates+=1
        if _type == "ipv4":
            addr = AddressIPv4(address[1])
        else:
            addr = AddressIPv6(address[1])

        if address[0] == 'A':
            val = RIB.SavePrefix(addr)
            if val:
                action = FIB.SavePrefix(addr)
                updateAnalyser.SaveAction(action)
                iter += 1
        
        if address[0] == 'W':
            result, r = DeletePrefix(RIB, addr)
            if result == True:
                action = FIB.DeletePrefix(addr)
                updateAnalyser.DeleteAction(action)
                iter += 1

        if iter == _iter:
            iter = 0
            print(updates)
            overallAnalyser.AddStatData(FIB.GetStatistics())

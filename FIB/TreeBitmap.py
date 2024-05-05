#This is an implementation of fixed miltibit trie algorithm, where stride lenght is equal to 3.
import GeneralObjects
from collections import defaultdict, deque

class ExternalBitmap:
    def __init__(self) -> None:
        self.array = {
            '000': 0,
            '001': 1,
            '010': 2,
            '011': 3,
            '100': 4,
            '101': 5,
            '110': 6,
            '111': 7}
        
        self.children = 8 * [None]
        self.childrenNum = 0
    
    def SaveChilde(self, _prefix, _mask): #predelat, maska neodpovida tomu, co se pak posila do message
        index = self.array[_prefix]
        if self.children[index] == None:
            self.children[index] = Node(_mask)
            self.childrenNum += 1
            return f"|{int(_mask/3)}#1"
        else:
            return f"|{int(_mask/3)}#0"
    
    def HasChildren(self):
        for ch in self.children:
            if ch != None:
                return True
        return False
    
    def DeleteChilde(self, _prefix):
        index = self.array[_prefix]
        try:
            self.children[index] = None
        except:
            print(len(self.children))
        self.childrenNum -= 1
    
class InternalBitmap:
    def __init__(self) -> None:
        self.prefixNum = 0
        self.array = {
            '*': False,
            '0*': False,
            '1*': False,
            '00*': False,
            '01*': False,
            '10*': False,
            '11*': False}
    
    def SavePrefix(self, _prefix):
        _prefix += '*'
        self.array[_prefix] = True
        self.prefixNum += 1

    def DeletePrefix(self, _prefix):
        _prefix += '*'
        self.array[_prefix] = False
        self.prefixNum -= 1

    def AnyPrefix(self):
        for element in self.array:
            if self.array[element] == True:
                return True
        return False

class Node:
    def __init__(self, _mask: int) -> None: 
        # If mask is for example 0, it means that the first bit of this stride has index 0 of the IP prefix.
        # The stride then corresponds to max number of bits, falling into this node. The interval of bits in 
        # IP prefix is then from mask to mask+SL
        
        self.mask = _mask
        self.internalBitmap = InternalBitmap()
        self.externalBitmap = ExternalBitmap()
    
    def _savePrefix(self, _addr: GeneralObjects.AddressIPv4):
        message = ""
        _prefix = ""
        if (self.mask+2) > _addr.mask:
            for i in range(0, 3):
                if i+self.mask > _addr.mask:
                    break
                else:
                    _prefix += str(_addr.GetBitValue(self.mask+i))
            self.internalBitmap.SavePrefix(_prefix)
            return ""
        else:
            for i in range(0, 3):
                v = str(_addr.GetBitValue(self.mask+i))
                _prefix += v
            
            index = self.externalBitmap.array[_prefix]
            message += self.externalBitmap.SaveChilde(_prefix, self.mask+3)
            return message + self.externalBitmap.children[index]._savePrefix(_addr)
            
    def _deletePrefix(self, _addr: GeneralObjects.AddressIPv4):
        message = ""
        _prefix = ""
        
        if (self.mask+2) > _addr.mask:
            for i in range(0, 3):
                if i+self.mask > _addr.mask:
                    break
                else:
                    _prefix += str(_addr.GetBitValue(self.mask+i))
            self.internalBitmap.DeletePrefix(_prefix)
            if self.internalBitmap.AnyPrefix() == False and self.externalBitmap.HasChildren() == False:
                return (True, f"|{int(self.mask/3)}#1")
            else:
                return (False, f"|{int(self.mask/3)}#0")
        else:
            for i in range(0, 3):
                v = str(_addr.GetBitValue(self.mask+i))
                _prefix += v

            index = self.externalBitmap.array[_prefix]
            if self.externalBitmap.children[index] != None:
                res, message = self.externalBitmap.children[index]._deletePrefix(_addr)
                if res:
                    self.externalBitmap.DeleteChilde(_prefix)
                elif message == None:
                    return (False, None)
            else:
                return (False, None)
            
        if self.internalBitmap.AnyPrefix() == False and self.externalBitmap.HasChildren() == False:
            return (True, f"|{int(self.mask/3)}#1" + message)
        else:
            return (False, f"|{int(self.mask/3)}#0" + message)

def _fibStatistics(_root: Node, _list):
    curent_mask = 0
    queue = deque()

    queue.append(_root)

    while queue:
        current_node:Node = queue.popleft()
        if current_node != None:
            if current_node.mask > curent_mask:
                curent_mask += 3
                _list.append([None])

            _list.append([current_node.internalBitmap.prefixNum, current_node.externalBitmap.childrenNum])

            for ch in current_node.externalBitmap.children:
                queue.append(ch)

    _list.append(["END"])
    return

class TreeBitmap:
    def __init__(self):
        self.FIB = Node(0)

    def SavePrefix(self, _addr: GeneralObjects.AddressIPv4) -> str:
        message = self.FIB._savePrefix(_addr)
        return message

    def DeletePrefix(self, _addr: GeneralObjects.AddressIPv4) -> str:
        res, message = self.FIB._deletePrefix(_addr)
        if message == None:
            return ''
        return message

    def GetStatistics(self) -> list[tuple[bool, int]]:
        list = []
        _fibStatistics(self.FIB, list)
        return list
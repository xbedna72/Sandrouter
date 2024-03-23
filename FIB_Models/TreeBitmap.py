#This is an implementation of fixed miltibit trie algorithm, where stride lenght is equal to 3.

import GeneralObjects

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
    
    def SaveChilde(self, _prefix, _mask):
        index = self.array[_prefix]
        self.children[index] = Node(_mask)
        print(f"{_prefix} node created")
    
    def HasChilde(self, _prefix):
        index = self.array[_prefix]
        return True if self.children[index] != None else False
    
    def HasChildren(self):
        for ch in self.children:
            if ch != None:
                return True
        return False
    
    def DeleteChilde(self, _prefix):
        index = self.array[_prefix]
        del self.children[index]
        self.children[index] = None
    
class InternalBitmap:
    def __init__(self) -> None:
        self.array = {
            '0': False,
            '1': False,
            '00': False,
            '01': False,
            '10': False,
            '11': False,
            '000': False,
            '001': False,
            '010': False,
            '011': False,
            '100': False,
            '101': False,
            '110': False,
            '111': False}
    
    def SavePrefix(self, _prefix):
        for element in self.array:
            if element.startswith(_prefix):
                self.array[element] = True

    def DeletePrefix(self, _prefix):
        for element in self.array:
            if element.startswith(_prefix):
                self.array[element] = False

    def AnyPrefix(self):
        for element in self.array:
            if self.array[element] == True:
                return True
        
        return False

class Node:
    def __init__(self, mask: int) -> None: 
        # If mask is for example 0, it means that the first bit of this stride has index 0 of the IP prefix.
        # The stride then corresponds to max number of bits, falling into this node. The interval of bits in 
        # IP prefix is then from mask to mask+SL
        
        self.mask = mask
        print(f"Node created {self.mask}")
        self.internalBitmap = InternalBitmap()
        self.externalBitmap = ExternalBitmap()
    
    def _savePrefix(self, _addr: GeneralObjects.Address):
        _prefix = ""
        if (self.mask+3) > _addr.mask:
            for i in range(0, 3):
                if i+self.mask > _addr.mask:
                    break
                else:
                    _prefix += str(_addr.GetBitValue(self.mask+i))
            self.internalBitmap.SavePrefix(_prefix)
        else:
            for i in range(0, 3):
                v = str(_addr.GetBitValue(self.mask+i))
                _prefix += v
            
            if not self.externalBitmap.HasChilde(_prefix):
                self.externalBitmap.SaveChilde(_prefix, self.mask+3)

            index = self.externalBitmap.array[_prefix]
            self.externalBitmap.children[index]._savePrefix(_addr)
            
    def _deletePrefix(self, _addr: GeneralObjects.Address):
        _prefix = ""
        if (self.mask+3) > _addr.mask:
            for i in range(0, 3):
                if i+self.mask > _addr.mask:
                    break
                else:
                    _prefix += str(_addr.GetBitValue(self.mask+i))
            self.internalBitmap.DeletePrefix(_prefix)
            if self.internalBitmap.AnyPrefix() == False and self.externalBitmap.HasChildren() == False:
                return True
        else:
            for i in range(0, 3):
                v = str(_addr.GetBitValue(self.mask+i))
                _prefix += v

            index = self.externalBitmap.array[_prefix]
            if self.externalBitmap.children[index]._deletePrefix(_addr) == True:
                self.externalBitmap.DeleteChilde(_prefix)
            
            if self.internalBitmap.AnyPrefix() == False and self.externalBitmap.HasChildren() == False:
                return True

        return False
            

class TreeBitmap:
    def __init__(self) -> None:
        self.FIB = Node(0)

    def SavePrefix(self, _addr: GeneralObjects.Address):
        pass

    def DeletePrefix(self, _addr: GeneralObjects.Address):
        pass




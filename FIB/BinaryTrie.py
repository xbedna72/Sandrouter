import GeneralObjects
from collections import defaultdict, deque

class Node:
    def __init__(self, _mask: int):
        self.mask = _mask
        self.left = None
        self.right = None
        self.children_num = 0
        self.prefix: bool = False

    def SetLeft(self, _mask):
        if self.left == None:
            self.left = Node(_mask)
            self.children_num += 1
            return f"|{_mask}#1"
        else:
            return f"|{_mask}#0"

    def SetRight(self, _mask):
        if self.right == None:
            self.right = Node(_mask)
            self.children_num += 1
            return f"|{_mask}#1"
        else:
            return f"|{_mask}#0"
    
    def EmptySubtree(self) -> bool:
        if self.children_num == 0 and self.prefix == False:
            return True
        return False
    
    def _savePrefix(self, _addr: GeneralObjects.AddressIPv4) -> str:
        message = ""
        if self.mask == _addr.mask:
            self.prefix = True
            return message

        if _addr.GetBitValue(self.mask) == 1:
            message = self.SetRight(self.mask + 1)
            return message + self.right._savePrefix(_addr)
        else:
            message = self.SetLeft(self.mask + 1)
            return message + self.left._savePrefix( _addr)
     
class BinaryTrie:
    FIB: Node = None

    def __init__(self):
        self.FIB = Node(0)

    def SavePrefix(self, _addr: GeneralObjects.AddressIPv4) -> str:
       mes = self.FIB._savePrefix( _addr)
       return mes
    
    def DeletePrefix(self, _addr: GeneralObjects.AddressIPv4) -> str:
        res, mes = _deletePrefix(self.FIB, _addr)
        if mes == None:
            return ''
        return mes
    
    def GetStatistics(self) -> list[tuple[bool, int]]:
        list = []
        _fibStatistics(self.FIB, list)
        return list
    
    def FindPrefix(self, _addr):
        return _findPrefix(self.FIB, _addr)


def _findPrefix(root: Node, _addr: GeneralObjects.AddressIPv4):
    if root == None:
        return False
    
    if root.mask == _addr.mask:
        return root.prefix
    
    if _addr.GetBitValue(root.mask) == 1:
        return _findPrefix(root.right, _addr)
    else:
        return _findPrefix(root.left, _addr)

def _deletePrefix(root: Node, _addr: GeneralObjects.AddressIPv4) -> str:
    message = ""

    if root == None:
        return (False, None)

    if root.mask == _addr.mask:
        root.prefix = False
        if root.EmptySubtree():
            return (True, f"|{root.mask}#1|")
        else:
            return (False, f"|{root.mask}#0|")
            
    if _addr.GetBitValue(root.mask) == 1:
        res, message = _deletePrefix(root.right, _addr)
        if res:
            root.children_num -= 1
            root.right = None
        elif message == None:
            return res, message
    else:
        res, message =_deletePrefix(root.left, _addr)
        if res:
            root.children_num -= 1
            root.left = None
        elif message == None:
            return res, message
    
    if root.EmptySubtree():
        return (True, f"|{root.mask}#1" + message)
    else:
        return (False, f"|{root.mask}#0" + message)

def _fibStatistics(_root:Node, _list: list):
    curent_mask = 0
    queue = deque()

    queue.append(_root)

    while queue:
        current_node:Node = queue.popleft()
        if current_node != None:
            if current_node.mask > curent_mask:
                curent_mask += 1
                _list.append([None])

            _list.append([(1 if current_node.prefix == True else 0), current_node.children_num])

            queue.append(current_node.left)
            queue.append(current_node.right)

    _list.append(["END"])
    return
    

import GeneralObjects
from collections import defaultdict, deque

class Node:
    def __init__(self, _mask: int):
        self.mask = _mask
        self.left = None
        self.right = None
        self.prefix: bool = False

    def SetLeft(self, _mask):
        if self.left == None:
            self.left = Node(_mask)
            return f"|{_mask}#1"
        else:
            return f"|{_mask}#0"

    def SetRight(self, _mask):
        if self.right == None:
            self.right = Node(_mask)
            return f"|{_mask}#1"
        else:
            return f"|{_mask}#0"
    
    def EmptySubtree(self)->bool:
        if self.right == self.left == None and self.prefix == False:
            return True
        return False
    
    def _savePrefix(self, _addr: GeneralObjects.Address):
        if self.mask == _addr.mask:
            self.prefix = True
            return ""

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

    def SavePrefix(self, _addr: GeneralObjects.Address):
       return self.FIB._savePrefix( _addr)
    
    def DeletePrefix(self, _addr: GeneralObjects.Address):
        res, mes = _deletePrefix(self.FIB, _addr)
        return mes
    
    def GetStatistics(self) -> list:
        list = []
        _fibStatistics(self.FIB, list)
        return list

def _deletePrefix(root: Node, _addr: GeneralObjects.Address):
    message = ""
    if root.mask == _addr.mask:
        root.prefix = False
        if root.EmptySubtree():
            return (True, f"|{root.mask}#1|")
        else:
            return (False, f"|{root.mask}#0|")

    if _addr.GetBitValue(root.mask) == 1:
        res, message = _deletePrefix(root.right, _addr)
        if res:
            del root.right
            root.right = None
    else:
        res, message =_deletePrefix(root.left, _addr)
        if res:
            del root.left
            root.left = None
    
    if root.EmptySubtree():
        return (True, f"|{root.mask}#1" + message)
    else:
        return (False, f"|{root.mask}#0" + message)

def _fibStatistics(_root:Node, _list: list):
    curent_mask = 0
    queue = deque()

    queue.append(_root)

    while queue:
        current_node = queue.popleft()
        if current_node != None:
            if current_node.mask > curent_mask:
                curent_mask += 1
                _list.append([None])

            if current_node.left == None and current_node.right == None:
                _list.append([current_node.prefix, 0])
            elif current_node.left != None and current_node.right != None:
                _list.append([current_node.prefix, 2])
            else:
                _list.append([current_node.prefix, 1])

            queue.append(current_node.left)
            queue.append(current_node.right)

    _list.append([None])
    return
    
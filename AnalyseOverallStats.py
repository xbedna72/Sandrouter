import GraphGenerator as grg

class Level:
    def __init__(self, _index):
        self.nodesNumber = []
        self.nodesWithPrefixNumber = []
        self.leaves = []
        self.maxChildren = []
        self.maxPrefixes = []
        self.level = _index
    
    def __str__(self) -> str:
        return f'{self.level}::{self.nodesNumber}:{self.maxPrefixes}:{self.nodesWithPrefixNumber}:{self.leaves}:{self.maxChildren}\n'

class OverallAnalyser:
    def __init__(self):
        self.Data = []
    
    def AddStatData(self, _list):
        index = 0
        if len(self.Data) == 0:
            self.Data.append(Level(index))
        
        _nodesNumber = 0
        _nodesWithPrefixNumber = 0
        _leaves = 0
        _maxNumberOfChildren = 0
        _maxPrefixes = 0

        for node in _list:
            if node[0] == None:
                self.Data[index].nodesNumber.append(_nodesNumber)
                self.Data[index].nodesWithPrefixNumber.append(_nodesWithPrefixNumber)
                self.Data[index].leaves.append(_leaves)
                # I am interested in the maximum amount of storage
                # I need to alocate for each node.
                self.Data[index].maxChildren.append(_maxNumberOfChildren)
                self.Data[index].maxPrefixes.append(_maxPrefixes)
                _nodesNumber = 0
                _nodesWithPrefixNumber = 0
                _leaves = 0
                _maxNumberOfChildren = 0
                _maxPrefixes = 0
                index += 1
                if index == len(self.Data):
                    self.Data.append(Level(index))
            elif node[0] == "END":
                self.Data[index].nodesNumber.append(_nodesNumber)
                self.Data[index].nodesWithPrefixNumber.append(_nodesWithPrefixNumber)
                self.Data[index].leaves.append(_leaves)
                # I am interested in the maximum amount of storage (for children or for prefix pointers)
                # I need to alocate for each node.
                self.Data[index].maxChildren.append(_maxNumberOfChildren)
                self.Data[index].maxPrefixes.append(_maxPrefixes)
            else:
                _nodesNumber += 1
                if node[0] > 0:
                    _nodesWithPrefixNumber += 1
                if node[0] > _maxPrefixes:
                    _maxPrefixes = node[0]
                if node[1] == 0:
                    _leaves += 1
                if node[1] > _maxNumberOfChildren:
                    _maxNumberOfChildren = node[1]
    
    def GetNumberOfNodesEachLevel(self):
        result = []

        for level in self.Data:
            result.append(level.nodesNumber)
        
        return result

    def GenerateStatistics(self, _folder):
        D_nodesNumber = grg.Data(_folder)
        D_maxPrefixes = grg.Data(_folder)
        D_nodesWithPrefixNumber = grg.Data(_folder)
        D_leaves = grg.Data(_folder)
        D_maxChildren = grg.Data(_folder)
        
        for d in self.Data:
            D_nodesNumber.AddData(d.nodesNumber)
            D_maxPrefixes.AddData(d.maxPrefixes)
            D_nodesWithPrefixNumber.AddData(d.nodesWithPrefixNumber)
            D_leaves.AddData(d.leaves)
            D_maxChildren.AddData(d.maxChildren)
        
        D_nodesNumber.GenerateGrapth("nodes_number", "log")
        D_maxPrefixes.GenerateGrapth("maximum_prefixes", "-")
        D_nodesWithPrefixNumber.GenerateGrapth("number_of_prefix_nodes", "log")
        D_leaves.GenerateGrapth("number_of_leaves", "log")
        D_maxChildren.GenerateGrapth("maximum_children", "-")

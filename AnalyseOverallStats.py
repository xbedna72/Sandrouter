import sys
import json
import os
import matplotlib.pyplot as plt
from pathlib import Path

class Level:
    def __init__(self):
        self.nodesNumber = []
        self.nodesWithPrefixNumber = []
        self.leafs = []
        self.children = []

class OverallAnalyser:
    def __init__(self):
        self.iteration = 0
        self.Data = []
    
    def AddStatData(self, _list):
        print("Adding statistics")
        index = 0
        if len(self.Data) == 0:
            self.Data.append(Level())
        
        _nodesNumber = 0
        _nodesWithPrefixNumber = 0
        _leafs = 0
        _children = []

        for element in _list:
            if element[0] == None:
                self.Data[index].nodesNumber.append(_nodesNumber)
                self.Data[index].nodesWithPrefixNumber.append(_nodesWithPrefixNumber)
                self.Data[index].leafs.append(_leafs)
                self.Data[index].children.append(_children)
                _nodesNumber = 0
                _nodesWithPrefixNumber = 0
                _leafs = 0
                _children.clear()
                index += 1
                if index == len(self.Data):
                    self.Data.append(Level())
            else:
                _nodesNumber += 1
                if element[0] == True:
                    _nodesWithPrefixNumber += 1
                if element[1] == 0:
                    _leafs += 1
                _children.append(element[1]) 
    
    def GenerateStatistics(self):
        _path = "./SandRouterProject/statistics/overall_statistics.out"
        targetFile = Path(_path)
        fileHandle = open(_path, "w")
        

        

        

        

        

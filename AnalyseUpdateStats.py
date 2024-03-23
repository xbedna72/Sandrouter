import os

def ParseLine(_line:str) -> list[(int, str)]:
    parsedLine = _line.split('|')
    output = []

    for step in parsedLine:
        component = step.split('#')
        if len(component) > 1:
            action = False if component[1] == "0" else True
            output.append((int(component[0]), action))
    
    return output

class AnalyseProperties:
    updates = 0
    depths = []
    modifiedNodes = 0
    addressNotFound = 0
    action_updates_array = []

    def __init__(self):
        self.action_updates_array = [0]

class UpdatesAnalyser:
    properties = []       #id 0 = save, id 1 = delete

    def __init__(self):
        self.properties.append(AnalyseProperties())
        self.properties.append(AnalyseProperties())
    
    def SaveAction(self, line):
        self._Action(line, 0)    

    def DeleteAction(self, line):
        self._Action(line, 1)

    def _Action(self, line, id):
        action = ParseLine(line)
        self.properties[id].updates = self.properties[id].updates + 1
        self.properties[id].depths.append(len(action))
        
        for step in action:
            if step[1] == True:
                self.AddAction(step[0], id)

    def AddAction(self, level, id):
        if len(self.properties[id].action_updates_array) < (level+1):
            for i in range(0, (level + 1) - len(self.properties[id].action_updates_array)):
                self.properties[id].action_updates_array.append(0)

        self.properties[id].modifiedNodes = self.properties[id].modifiedNodes + 1
        self.properties[id].action_updates_array[level] = self.properties[id].action_updates_array[level] + 1

    def FinishAnalyse(self, _file: str):
        fileHandle = open(_file, "w")

        fileHandle.write("SAVE UPDATES ::\n")
        actionUpdates = self.properties[0].updates  
        for i in range(0, len(self.properties[0].action_updates_array)):
            fileHandle.write(f"level {i}: {self.properties[0].action_updates_array[i]} ({((self.properties[0].action_updates_array[i]/actionUpdates) *100):2.2f}%)\n")
        fileHandle.write(f"created nodes: {self.properties[0].modifiedNodes}\n")
        fileHandle.write(f"all updates: {self.properties[0].updates}\n")
        fileHandle.write(f"created nodes per action update: {self.properties[0].modifiedNodes/actionUpdates}\n")
        allDepth = 0
        max = 0
        min = len(self.properties[0].action_updates_array)

        for d in self.properties[0].depths:
            allDepth = allDepth + d
            if max < d:
                max = d
            if min > d:
                min = d

        fileHandle.write(f"averageDepth: {allDepth/self.properties[0].modifiedNodes}\n")
        fileHandle.write(f"min depth: {min}\n")
        fileHandle.write(f"max depth: {max}\n")

        fileHandle.write("\n")
        fileHandle.write("DELETE UPDATES ::\n")
        actionUpdates = self.properties[1].updates
        for i in range(0,len(self.properties[1].action_updates_array)):
            fileHandle.write(f"level {i}: {self.properties[1].action_updates_array[i]} ({((self.properties[1].action_updates_array[i]/actionUpdates) *100):2.2f}%)\n")
        fileHandle.write(f"deleted nodes: {self.properties[1].modifiedNodes}\n")
        fileHandle.write(f"all updates: {self.properties[1].updates}\n")
        fileHandle.write(f"deleted nodes per action update: {self.properties[1].modifiedNodes/actionUpdates}\n")
        allDepth = 0
        max = 0
        min = len(self.properties[1].action_updates_array)

        for d in self.properties[1].depths:
            allDepth = allDepth + d
            if max < d:
                max = d
            if min > d:
                min = d

        fileHandle.write(f"averageDepth: {allDepth/self.properties[1].modifiedNodes}\n")
        fileHandle.write(f"min depth: {min}\n")
        fileHandle.write(f"max depth: {max}\n")


        fileHandle.close()

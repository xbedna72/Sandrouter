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
    def __init__(self):
        self.action_updates_array = [0]
        self.updates = 0
        self.depths = []
        self.modifiedNodes = 0

class UpdatesAnalyser:
    properties = []       #id 0 = save, id 1 = delete

    def __init__(self):
        self.properties.append(AnalyseProperties())
        self.properties.append(AnalyseProperties())
        self.levels = []
    
    def SaveAction(self, line):
        self._Action(line, 0)

    def DeleteAction(self, line):
        if len(line) > 0:
            self._Action(line, 1)

    def _Action(self, line, id):
        action = ParseLine(line)
        
        self.properties[id].updates += 1
        if id == 1:
            self.properties[id].depths.append(len(action)-1)
        else:
            self.properties[id].depths.append(len(action))
    
        for step in action:
            if step[1] == True:
                self.AddAction(step[0], id)

    def AddAction(self, level, id):
        if len(self.properties[id].action_updates_array) < (level+1):
            for i in range(0, (level + 1) - len(self.properties[id].action_updates_array)):
                self.properties[id].action_updates_array.append(0)

        self.properties[id].modifiedNodes += 1
        self.properties[id].action_updates_array[level] += 1

        if len(self.levels) < (level+1):
            for i in range(0, (level + 1) - len(self.levels)):
                self.levels.append([0])
        
        val = self.levels[level][-1]
        if id == 0:
            self.levels[level].append(val+1)
        else:
            self.levels[level].append(val-1)

    def FinishAnalyse(self, _file: str):
        fileHandle = open(_file, "+w")

        fileHandle.write("-----------------------------------------------------------------------------\n")
        fileHandle.write("     |    SAVE UPDATES    |    DELETE UPDATES    |   Total number of nodes   \n")
        fileHandle.write("-----------------------------------------------------------------------------\n")
        deleteUpdates = self.properties[1].updates
        saveUpdates = self.properties[0].updates
        fileHandle.write("Level|    Updates      %  |      Updates      %  |        Min       Max\n")
        
        insert_list_length = len(self.properties[0].action_updates_array)
        delete_list_length = len(self.properties[1].action_updates_array)
        _ar = insert_list_length if insert_list_length > delete_list_length else delete_list_length
        for i in range(0, _ar):
            line=""
            
            line+=f"{i:3}. |"

            if i < insert_list_length:
                line+=f"{self.properties[0].action_updates_array[i]:7}"
                line+=f"{((self.properties[0].action_updates_array[i]/saveUpdates) *100):10.0f}% |"
            else:
                line+=f"                      |"

            if i < delete_list_length:
                line+=f"{self.properties[1].action_updates_array[i]:10}"
                line+=f"{((self.properties[1].action_updates_array[i]/deleteUpdates) *100):10.0f}% |"
            else:
                line+=f"                      |"

            line+=f"{min(self.levels[i]):10}{max(self.levels[i]):10}\n"
            fileHandle.write(line)
                    
        fileHandle.write("-----------------------------------------------------------------------------\n")
        fileHandle.write(f"     Number of updates:{saveUpdates:3}|Number of updates:{deleteUpdates:3} |\n")
        fileHandle.write(f"     Created nodes:{self.properties[0].modifiedNodes:3}    |Removed nodes:{self.properties[1].modifiedNodes:3}\n")

        fileHandle.write(f"     min depth:{min(self.properties[0].depths):3}        |min depth:{min(self.properties[1].depths):3}\n")
        fileHandle.write(f"     max depth:{max(self.properties[0].depths):3}        |max depth:{max(self.properties[1].depths):3}\n")

        fileHandle.close()

import sys
import os
from pathlib import Path
import Definition
from AnalyseUpdateStats import UpdatesAnalyser
from AnalyseOverallStats import OverallAnalyser
       
if __name__ == "__main__":
    targetFile = ''
    try:
        targetFile = Path(sys.argv[2])
        print(f"INFO: Target file from path {sys.argv[2]} was created.")
    except:
        print("ERROR: Unable to generate target file path.")
        exit(-1)

    RIB, FIB = Definition.GenerateTables_BinarieTrieFIB(sys.argv[1])
    updatesAnalyser = UpdatesAnalyser()
    overallAnalyser = OverallAnalyser()
    
    for i in range(3, len(sys.argv)):
        Definition.PutUpdates(sys.argv[i], RIB, FIB, updatesAnalyser, overallAnalyser)
        print(f"{sys.argv[i]} DONE")
    
    #updatesAnalyser.FinishAnalyse(sys.argv[2])
    overallAnalyser.GenerateStatistics()
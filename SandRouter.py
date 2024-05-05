import argparse
from pathlib import Path
import Manager
from AnalyseUpdateStats import UpdatesAnalyser
from AnalyseOverallStats import OverallAnalyser

class FilePaths:
    def __init__(self, _folder):
        self.graphs_folder = Path(f"{_folder}/graphs/")
        if self.graphs_folder.exists() == False:
            self.graphs_folder.mkdir(parents=True)
            print(f"INFO: Folders for statistics storage, {_folder} and {self.graphs_folder}, were created.")
        else:
            print(f"INFO: Folders '{_folder}' and '{self.graphs_folder}', already exist.")

        self.statistics_file = Path(f"{_folder}/dynamic_statistics.out")
        if self.statistics_file.exists() == False:
            self.statistics_file.touch()
            print(f"INFO: Update statistic file '{self.statistics_file}' was created.")
        else:
            print(f"INFO: Update statistic file already exists. The file will be overridden.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='SandRouter', 
                                     description='SandRouter is an application, developed as a benchmark tool to help evaluate behavior of the Longest Prefix Matching algorithms.'+
                                    ' The simulation could be configured based on provided input parameters.')
    parser.add_argument('-m','--model', choices=[0,1,2], default=0, type=int, help='Selection of the benchmarked model. Values: 0-BinaryTrie, 1-TreeBitmap, 2-FIBModel. Defaul value: 0')
    parser.add_argument('-c', '--count', help='Number of updates after which will be executed overall analyzation of the model data structure.'+
                        ' Attention: If the simulation takes too much time, there is a possibility, that number of updates processed by FIB module is too large. In this way, consider set up higher period between analyzations.',
                        type=int, default=1)
    parser.add_argument('-b', '--base', type=str, help='Path of a file containing the base BGP snapshot, with which will be the FIB table initialized.', required=True)
    parser.add_argument('-u', '--updates', type=str, default="", help='Path of a file containing preprepared BGP messages for the simulation.', required=True)
    parser.add_argument('-d', '--destination', type=str, help='Path of a folder, where final statistics will be saved.', required=True)
    parser.add_argument('-t', '--type', type=str, choices=["ipv4", "ipv6"], help='The type of addresses passed in base file and updates file.', required=True)

    args = parser.parse_args()

    fp = FilePaths(args.destination)
    
    RIB, FIB = Manager.GenerateTables(args.base, args.model, args.type)
    print("INFO::Base structure of RIB and FIB model prepared.")
    updatesAnalyser = UpdatesAnalyser()
    overallAnalyser = OverallAnalyser()
    
    Manager.PutUpdates(args.updates, RIB, FIB, updatesAnalyser, overallAnalyser, args.count, args.type)
    print("INFO::Benchmark finished. Preparation for dynamic statistic generation.")
    updatesAnalyser.FinishAnalyse(fp.statistics_file)
    print("INFO::Dynamic statistics genertaion finished. Preparation for graph generation into folder graphs.")
    
    overallAnalyser.GenerateStatistics(fp.graphs_folder)
    print("INFO::Graphs generation, finished. Benchmark, finished.")
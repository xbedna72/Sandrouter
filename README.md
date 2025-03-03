This project was developed as a practical part for thesis: *Framework for Analysis of Changes in Data Structures of Core Routers*

Abstract
---
Core routers have to be able to work at high speed to keep up with the demands of new Internet services and applications. One of the factors is the classification algorithm utilized in a router in the process of forwarding incoming packets based on their destination IP addresses. Each address is provided to the Forwarding Information Base (FIB) table, which implements the Longest Prefix Matching algorithm (LPM). The FIB table stores prefixes which represents reachable networks. Based on the provided IP address, the FIB table can decide in which way the packet should continue to reach the final destination. There are many LPM algorithms, and each can provide different properties, such as search speed, storage requirements, complexity of updates, etc. The FIB table is constructed from Routing Information Base (RIB) and during the operation of the router, both structures
are updated based on the routing information exchanged between routers. In this sense, the thesis focuses on how the data structures of the FIB tables are changed in core routers. The thesis proposes a benchmark framework that helps to show how different LPM algorithms behave in the context of changes of the FIB data structures. The benchmark is done by simulation, where the LPM algorithm is put in the simplified router model. Then, using the Border Gateway Protocol (BGP) messages, the algorithm modifies the FIB data structure. The whole simulation is monitored and the effects of changes are stored. At the end of the simulation, statistical results are generated. Finally, the framework provides a functionality to change the LPM algorithm and other simulation parameters. The final result is then verified by multiple experiments.

Description
---
![sandrouter_design](https://github.com/user-attachments/assets/42861293-bef9-4ff5-af66-0e8cd8b35197)

The tool processes BGP communication and simulates data flow over RIB table (```./RIB.py```) and FIB table (```./FIB/..```). During simulation, the FIB table is updated and this changes are stored for further analyzation. From stored information the tool generate statistics in form of graphs, at the end of a simulation.

The tool provide implementation for both IP protocol versions, v4 and v6. There are also already provided two implementations of FIB table: Tree Bitmap and Binary Trie.

Execution
---

SandRouter is an application, developed as a benchmark tool to help evaluate behavior of the Longest Prefix Matching algorithms. This repository already contains two implementations of LPM algorithms (see ```./FIB/```). There you can also find ```./FIB/FIBModel.py```, where can be added new implementation for testing. The simulation could be configured based on provided input parameters:

-  -m, --model - Selection of the benchmarked model. Values: 0-BinaryTrie, 1-TreeBitmap, 2-FIBModel. Defaul: 0
-  -c, --count - Number of updates after which will be executed overall analyzation of the model data structure. Attention: If the simulation takes too much time, there is a possibility, that number of updates processed by FIB module is too large. In this way, consider set up higher period between analyzations.
-  -b, --base - Path of a file containing the base BGP snapshot, with which will be the FIB table initialized.
-  -u, --updates - Path of a file containing preprocessed BGP messages for the simulation.
-  -d, --destination - Path of a folder, where final statistics will be saved.
-  -t', --type - choices=["ipv4", "ipv6"] - The type of addresses passed in base file and updates file.

Example: ```python3 SandRouter.py -m 0 -b "LACNIC_base.txt" -u "LACNIC_updates.txt" -d "../BT/LACNIC/${collector}"```

Base file and updates file can be preprocessed by script ```./scripts/SandRouter_preprocessing.sh```. For execution information see help message.

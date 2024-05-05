import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class Data:
    def __init__(self, _folder):
        self.folder = _folder
        self.array = []
    
    def AddData(self, _array):
        self.array.append(_array)

    def GenerateGrapth(self, name, scale):    
        fig = plt.figure(figsize=(20, 8))
        ax = fig.add_subplot(111)
        ax.set_ylabel('Value')
        ax.set_xlabel('Level/Mask')
        ax.boxplot(self.array)
        ax.set_xticklabels(range(0, len(self.array)))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.title(name)
        plt.yticks(fontsize=12)
        plt.xticks(rotation=-90, fontsize=8)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        plt.savefig(f"{self.folder}/{name}.png")
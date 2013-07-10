import matplotlib.pyplot as plt
from memory_profiler import LineProfiler
import inspect 
import numpy as np
import matplotlib.gridspec as gridspec
import gc 
import multiprocessing
class MemoryProfiler(object):
    def __init__(self, profileMethod, runfunc):
        self.profileMethod = profileMethod
        cls = profileMethod.im_class
        methString = profileMethod.func_name
        setattr(cls, methString, self.decorate(getattr(cls, methString)))
        self.runfunc = runfunc
        self.codeMap = dict()
       
    def decorate(self, func):
        def wrapper(*args, **kwargs):
            gc.collect()
            prof = LineProfiler()
            out = prof(func)(*args, **kwargs)
           # self.codeMap.update(prof.code_map)
            self.codeMap = prof.code_map
            return out
        return wrapper
 
    @property
    def maxMemory(self):
        maxitem = 0
        for value in self.codeMap.values():
            for maxval in value.values():
                maxitem = max(max(maxval), maxitem)
        return maxitem

    def getMethodName(self):
        return self.profileMethod.__name__

    #using the keys get the memory for a specified line
    def getLineMemory(self, line=15):

        max_mem = 0
        count = 1
        keys = self.codeMap.values()[0].keys()
        breaker = True
        while breaker == True:
            if line in keys:
                max_mem = max(self.codeMap.values()[0][line])
                breaker = False
            else:
                if count % 2 == 1:
                    line = line + count
                    count += 1
                else:
                    line = line - count
                    count += 1
        return max_mem           
        
                 
    def profile(self, *args, **kwargs):
        gc.collect()
        self.runfunc(*args, **kwargs)

class MemoryViewer(object):
    def __init__(self, ncells, regenerate=False):
        self.ncells = ncells

    # def getMemoryValues(self, profileMethod, runfunc, line, ncell):
    #     def worker(ncell, resultQ, lines, profileMethod, runfunc):
    #         from profiling_memory import MemoryProfiler
    #         m = MemoryProfiler(profileMethod, runfunc)
    #         m.profile(ncell)
    #         resultQ.put([m.maxMemory] + [m.getLineMemory(l) for l in lines])

    #     resultQ = multiprocessing.Queue()
    #     process = multiprocessing.Process(target=worker, args=(ncell, resultQ, (line,), profileMethod, runfunc))
    #     process.start()
    #     resultList = resultQ.get()
    #     return resultList[0], resultList[1]

    # def getMemoryList(self, profileMethod, runfunc, line, ncells):
    #     return [self.getMemoryValues(profileMethod, runfunc, line, ncell) for ncell in ncells]

    # def calcAndPlot(self, profileMethod, runfunc, line, ncells):
    #     a = np.array(self.getMemoryList(profileMethod, runfunc, line, ncells))
    #     lineMemoryValues, allMemory = np.swapaxes(a, 1, 0)
    #     self.plot(lineMemoryValues, allMemory, profileMethod, line, ncells)

    def plot(self, profileMethod, runfunc, line):
        
        fig = plt.figure()
        gs = gridspec.GridSpec(2,1)
        ax1 = plt.subplot(gs[1, :-1])

        lineMemoryValues = []
        allMemory = []

        def worker(ncell, resultQ, lines, profileMethod, runfunc):
            from profiling_memory import MemoryProfiler
            m = MemoryProfiler(profileMethod, runfunc)
            m.profile(ncell)
            resultQ.put([m.maxMemory] + [m.getLineMemory(l) for l in lines])
        
        
        for ncell in self.ncells:
            resultQ = multiprocessing.Queue()
            process = multiprocessing.Process(target=worker, args=(ncell, resultQ, (line,), profileMethod, runfunc))
            process.start()
            resultList = resultQ.get()
            lineMemoryValues.append(resultList[1])
            allMemory.append(resultList[0])
           # raw_input("stop")

        label = "Line Profile:" + profileMethod.__name__ + " Line : " + str(line)
        print lineMemoryValues
        ax1.loglog(self.ncells, lineMemoryValues, label=label)

        label = "Full Profile:" + profileMethod.__name__
        print allMemory
        ax1.loglog(self.ncells, allMemory, label=label)
        plt.xlabel("ncells")
        plt.ylabel("maximum memory values (MB)")
        
        gs.tight_layout(fig, rect=[0,0,1,1])
       # plt.loglog(self.ncells, self.ncells**2, label="$ncells^2$")
       # plt.loglog(self.ncells, self.ncells*np.log(self.ncells), label="nlogn")
        plt.xlabel("ncells")
        plt.ylabel("maximum memory values (MB)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, ncol=1, mode="wrap", borderaxespad=0., prop={'size': 12})
        plt.show()
 
if __name__ == '__main__':

    from polyxtal import PolyxtalSimulation
    from polyxtal import func

    #from coupled1D import CoupledSimulation
    #from coupled1D import func

    ncells = np.array(np.logspace(4, 5, 5), dtype=int)
   # ncells = np.ones(5, dtype=int)*10000
    memoryViewer = MemoryViewer(ncells)
    memoryViewer.plot(PolyxtalSimulation.setup, func, line=15)
    #memoryProfiler = MemoryProfiler(profileMethod=PolyxtalSimulation.setup, runfunc=func)
    #memoryViewer = MemoryViewer(memoryProfiler, ncells)
   
    plt.show()

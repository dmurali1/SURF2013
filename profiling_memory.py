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
    def __init__(self, ncells, profileMethod, runfunc, lines, regenerate=False):
        self.ncells = ncells
        self.profileMethod = profileMethod
        self.runfunc = runfunc
        self.lines = lines

    def generateData(self):
        def worker(ncell, resultQ, profileMethod, runfunc, lines):
            from profiling_memory import MemoryProfiler
            m = MemoryProfiler(profileMethod, runfunc)
            m.profile(ncell)
            resultQ.put([m.maxMemory] + [m.getLineMemory(l) for l in lines])
        
        resultLists = []
        for ncell in self.ncells:
            resultQ = multiprocessing.Queue()
            process = multiprocessing.Process(target=worker, args=(ncell, resultQ, self.profileMethod, self.runfunc, self.lines))
            process.start()
            results = resultQ.get()
            resultLists.append(results)
        return resultLists

    def savedata(self, listOfResults, datafiles):
        for r, d in zip(listOfResults, datafiles):
            np.savetxt(d, r)
        
    def readdata(self, datafiles):
        return [np.loadtxt(d) for d in datafiles]

    def plot(self, data):
        
        memoryValues = np.array(data).swapaxes(0,1)
        labels = ["Full Profile:" + self.profileMethod.__name__]
        labels += ["Line Profile:" + self.profileMethod.__name__ + " Line : " + str(l) for l in self.lines]
        
        for label, memory in zip(labels, memoryValues):
            plt.loglog(self.ncells, memory, label=label)

        plt.xlabel("ncells")
        plt.ylabel("maximum memory values (MB)")
        
        plt.legend(loc="upper left")
        plt.show()

        plt.loglog(self.ncells, self.ncells**2, label="$ncells^2$")
        plt.loglog(self.ncells, self.ncells*np.log(self.ncells), label="nlogn")
 
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
    # def plotIP(self, data):
    #     fig = plt.figure()
    #     gs = gridspec.GridSpec(2,1)
    #     ax1 = plt.subplot(gs[1, :-1])
        
    #     allMemory, lineMemoryValues = np.array(data).swapaxes(0,1)

    #     label = "Line Profile:" + self.profileMethod.__name__ + " Line : " + str(lines)
    #     print lineMemoryValues
    #     ax1.loglog(self.ncells, lineMemoryValues, label=label)

    #     label = "Full Profile:" + methodName
    #     print allMemory
    #     ax1.loglog(self.ncells, allMemory, label=label)
    #     plt.xlabel("ncells")
    #     plt.ylabel("maximum memory values (MB)")
        
    #     gs.tight_layout(fig, rect=[0,0,1,1])
    #    # plt.loglog(self.ncells, self.ncells**2, label="$ncells^2$")
    #    # plt.loglog(self.ncells, self.ncells*np.log(self.ncells), label="nlogn")
    #     plt.xlabel("ncells")
    #     plt.ylabel("maximum memory values (MB)")
    #     plt.legend(bbox_to_anchor=(1.05, 1), loc=2, ncol=1, mode="wrap", borderaxespad=0., prop={'size': 12})
 
    #     gs.tight_layout(fig, rect=[0,0,1,1])
    #     plt.show()

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

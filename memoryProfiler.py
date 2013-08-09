from memory_profiler import LineProfiler
import inspect 
import numpy as np
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
        self.runfunc(*args, **kwargs)
 
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

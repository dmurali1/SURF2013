import matplotlib.pyplot as plt
from memory_profiler import LineProfiler
import inspect 
import numpy as np
 
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
            prof = LineProfiler()
            out = prof(func)(*args, **kwargs)
            self.codeMap.update(prof.code_map)
          #  print self.codeMap.values()[0].values()
          #  print self.codeMap.values()[0].get(11)
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
    def getLineMemory(self, line):

        print self.codeMap
        raw_input("before keys")
        
        # mem =  self.codeMap.values()[0]
        # max_mem = max(mem[line])
        
        keys = self.codeMap.values()[0].keys()

        max_mem = 0
        breaker = True
        while breaker == True:
            if line in keys:
                max_mem = max(self.codeMap.values()[0][line])
                breaker = False
            else: 
                line = line + 1
        return max_mem           
        
                 
    def profile(self, *args, **kwargs):
        self.runfunc(*args, **kwargs)
 
       
class MemoryViewer(object):
    def __init__(self, memoryProfiler, ncells, regenerate=True):
        self.ncells = ncells
        self.memoryProfiler = memoryProfiler
   
    def plot(self):
        maxMemoryValues = []
        for ncell in self.ncells:
            self.memoryProfiler.profile(ncell)
            maxMemoryValues.append(self.memoryProfiler.maxMemory)
        label = self.memoryProfiler.getMethodName()
        plt.loglog(self.ncells, maxMemoryValues, label=label)
    #    plt.loglog(self.ncells, self.ncells**2, label="$ncells^2$")
    #    plt.loglog(self.ncells, self.ncells*np.log(self.ncells), label="nlogn")
        plt.xlabel("ncells")
        plt.ylabel("maximum memory values (MB)")
        plt.legend(loc=2)
 
if __name__ == '__main__':
    # import fipy as fp
    # from fipy.terms.term import Term
    # import numpy as np
    # def run(ncell):
    #     m = fp.Grid1D(nx=ncell)
    #     v = fp.CellVariable(mesh=m)
    #     fp.DiffusionTerm().solve(v)
 
    from polyxtal import PolyxtalSimulation
    from polyxtal import func

    #from coupled1D import CoupledSimulation
    #from coupled1D import func

    ncells = np.array(np.logspace(1, 3, 2), dtype=int)
    memoryProfiler = MemoryProfiler(profileMethod=PolyxtalSimulation.setup, runfunc=func)
    for ncell in ncells:
        memoryProfiler.profile(ncell)
    memoryViewer = MemoryViewer(memoryProfiler, ncells)
    print memoryProfiler.getLineMemory(14)
  #  memoryViewer.plot()
    plt.show()

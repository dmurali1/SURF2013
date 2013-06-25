import matplotlib.pyplot as plt
from memory_profiler import LineProfiler
 
 
class MemoryProfiler(object):
    def __init__(self, profileMethod, runfunc):
        self.profileMethod = profileMethod
        cls = profileMethod.im_class
        methString = profileMethod.func_name
        setattr(cls, methString, self.decorate(getattr(cls, methString)))
        self.runfunc = runfunc
       
    def decorate(self, func):
        def wrapper(*args, **kwargs):
            prof = LineProfiler()
            out = prof(func)(*args, **kwargs)
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
 
    def profile(self, *args, **kwargs):
        self.runfunc(*args, **kwargs)
 
       
class MemoryViewer(object):
    def __init__(self, memoryProfiler, ncells, regenerate=False):
        self.ncells = ncells
        self.memoryProfiler = memoryProfiler
   
    def plot(self):
        maxMemoryValues = []
        for ncell in self.ncells:
            self.memoryProfiler.profile(ncell)
            maxMemoryValues.append(self.memoryProfiler.maxMemory)
 
        plt.loglog(self.ncells, maxMemoryValues)
        plt.xlabel("ncells")
        plt.ylabel("maximum memory values (MB)")
 
 
if __name__ == '__main__':
    import fipy as fp
    from fipy.terms.term import Term
    import numpy as np
    
    from polyxtal import PolyxtalSimulation
    from polyxtal import func

    def run(ncell):
        m = fp.Grid1D(nx=ncell)
        v = fp.CellVariable(mesh=m)
        fp.DiffusionTerm().solve(v)
 
    ncells = np.array(np.logspace(1, 5, 20), dtype=int)
    memoryProfiler = MemoryProfiler(profileMethod=PolyxtalSimulation.setup, runfunc=func)
    memoryViewer = MemoryViewer(memoryProfiler, ncells)
    memoryViewer.plot()
    plt.show()

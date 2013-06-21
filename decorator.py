#file: decorator.py
#practice creating a decorator function
import inspect 
import numpy as np
from memory_profiler import LineProfiler

class Decorate:

    def __init__(self, profile_method):
       
        cls = profile_method.im_class
        meth_name = profile_method.func_name
        setattr(cls, meth_name, self.decor(getattr(cls, meth_name)))

    def decor(self, func):
        def wrapper(*args, **kwargs):
            prof = LineProfiler()
            out = prof(func)(*args, **kwargs) 
            self.code_map = prof.code_map
            return out
        return wrapper

if __name__=='__main__':

    from polyxtal import PolyxtalSimulation
    from polyxtal import func
    from fipy.variables.variable import Variable
    polyxtal = PolyxtalSimulation()
    # Variable.__init__
    dec = Decorate(polyxtal.setup)
    #loop through ncells and pass ncell into runfunc

    ncells = np.array(np.logspace(1, 3, 5), dtype=int)
    map_dict = {}

    for ncell in ncells:
        func(ncell)
        map_dict[ncell] = dec.code_map
    print map_dict,

    # memory for mesh, intermediate variables, matrix and solve
    
    # how does memory scale for these things

    # how much memory per cell for large system
        # how does that equate to the number of floats per cell?

    # before mesh, after mesh, after intermediate variables, after solve

    # 

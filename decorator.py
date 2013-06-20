#file: decorator.py
#practice creating a decorator function
import inspect 
from memory_profiler import LineProfiler

class Decorate:

    def __init__(self, ncells, runfunc, profile_method):

        self.ncells = ncells
        self.runfunc = runfunc        
        cls = profile_method.im_class
        meth_name = profile_method.func_name
        setattr(cls, meth_name, self.decor(getattr(cls, meth_name)))
        

    def decor(self, func):
        def wrapper(*args, **kwargs):
            prof = LineProfiler()
            out = prof(func)(*args, **kwargs) 
#            for ncell in self.ncells:
            self.code_map = prof.code_map
            return out
        return wrapper

if __name__=='__main__':
    import package.test
    from package.test import Test
    from package.test import func
    # from polyxtal import PolyxtalSimulation
    # polyxtal = PolyxtalSimulation()
    # ncells = np.array(np.logspace(1, 3, 5), dtype=int)
    dec = Decorate(ncells, func, Test.method)
    print dec.runfunc()
    print dec.code_map

##find a way to make this work for multiple ncells!!!!

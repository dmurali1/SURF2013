#make a memory class 
#take memory profiler decorating fuction and put it in class
#have ability to put decorator on function passed in
from fipyprofile import FiPyProfile
from memory_profiler import LineProfiler
import matplotlib.pyplot as plt
import pickle
class FiPyProfileMemory(FiPyProfile):

    def __init__(self, runfunc, funcString, ncells, regenerate=False):
        self.code_map = dict()
        super(FiPyProfileMemory, self).__init__(runfunc, funcString, ncells, regenerate)

    def profile(self, ncell):

        prof = LineProfiler()
        prof(self.runfunc)(ncell)
        print prof.code_map, ncell
        f = open(self.datafilestring(ncell), "w")
        pickle.dump(prof.code_map, f)
        f.close()

    def get_code_map(self, ncell):
        f = open(self.datafilestring(ncell), "r")
        out = pickle.load(f)
        f.close()
        return out

    def datafilestring(self, ncell):
        return "data/{funcString}{ncell}.txt".format(funcString=self.funcString, ncell=ncell)

    def get_largest_value(self, ncell):
        maxitem = 0
        codemap = self.get_code_map(ncell)
        print "regenerated", codemap.keys()
        for value in codemap.values():
            print value
            for maxval in value.values():
                maxitem = max(max(maxval), maxitem)
            print maxitem
        return maxitem


    def plot(self):
        functionMemory = []
        for ncell in self.ncells:
            print ncell,
            functionMemory.append(self.get_largest_value(ncell))
        plt.loglog(self.ncells, functionMemory)
        plt.loglog((10**4, 10**6), (10**2, 10**4))
        plt.xlabel("ncells")
        plt.ylabel("MB")

#figure out why maxitem is the same for all ncells
#save data to a file so we don't have to regenerate each time 

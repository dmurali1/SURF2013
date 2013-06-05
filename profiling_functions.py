#file: profiling_functions.py

from fipy import Grid1D, CellVariable, TransientTerm, DiffusionTerm, Viewer
import cProfile
import pstats 
import os
import numpy as np
import matplotlib.pyplot as plt
import math


class FiPyProfile:
    def __init__(self, runfunc, ncells, regenerate=False):
        self.runfunc = runfunc
        self.ncells = ncells
        self.regenerate = regenerate

    def datafilestring(self, ncell):
        return "data/{runfunc}{ncell}.stats".format(runfunc=self.runfunc.func_name, ncell=ncell)

    def profile(self, ncell):
        runFuncString = 'self.runfunc(ncell={ncell})'.format(ncell=ncell)
        cProfile.runctx(runFuncString, globals(), locals(), filename=self.datafilestring(ncell))
        
    def get_stats(self, ncell):
        if not os.path.exists(self.datafilestring(ncell)) or self.regenerate:
            self.profile(ncell)
        return pstats.Stats(self.datafilestring(ncell))

    def get_total_time(self, ncell):
        sorted_stats = self.get_stats(ncell).sort_stats("cumulative")
        slowest_function_key = sorted_stats.fcn_list[0]
        return sorted_stats.stats[slowest_function_key][3]

    def get_time_for_function(self, function_key, ncell):
        return self.get_stats(ncell).stats[function_key][3]
        
    def get_key_from_function_name(self, function_name):
        pass

    def get_key_from_function_pointer(self, function_pointer):
        pass

    def plot(self):
        allTimes = []
        for ncell in self.ncells:
            print ncell,
            allTimes.append(self.get_total_time(ncell))  

        plt.loglog(self.ncells, allTimes, label = "full profile")        
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                   ncol=3, fancybox=True, shadow=True)




#gets profile of function passed in
def getProfileStats(runFunc, ncell=100, regenerate=False):
    filename = "data/{runFunc}{ncell}.stats".format(runFunc=runFunc.func_name, ncell=ncell)
    if not os.path.exists(filename) or regenerate:
        runFuncString = 'runFunc(ncell={ncell})'.format(ncell=ncell)
        cProfile.runctx(runFuncString, globals(), locals(), filename=filename)
    return pstats.Stats(filename)
       
#takes in function pointers and returns tuples       
def getTuple(pointers):
    pass
#calls getProfileStats, finds 10 worst profileFcns and their associated key tuples
def getStatTuples(runFunc):
    a  = getProfileStats(runFunc, ncell, regenerate=regenerate)
    tuples = []
    for keys in a.stats.keys():
        tuples.append(keys)


#calls a function to get a list of tuples and returns the value for each function
def getValues(runFunc, profileFunc):
    pass


def getFcnStats(importFile, ncell=100, fcns=[None], regenerate=False):
    a  = getProfileStats(importFile, ncell, regenerate=regenerate)
    for fcn in fcns:
        if fcn:
            return a.stats[getKey(a.stats, fcn.func_name)][3]
        else:
            a = a.sort_stats("cumulative")
            return a.stats[a.fcn_list[0]][3]


def plotStats(runFunc, ncells, fcns=[], regenerate=False):
    
    allTimes = []
    for ncell in ncells:
        print ncell,
        allTimes.append(getFcnStats(runFunc, ncell=ncell, regenerate=regenerate))  
        fcnName.append(getFcnStats(runFunc, ncell=ncell, fcnName=fcnName, regenerate=regenerate))
        
    plt.loglog(ncells, fcnName, label=fcnName.func_name)

 #   plt.loglog(ncells, .30 * ncells**2, label = "$n^2$")
 #   plt.loglog(ncells, .90 * (ncells * np.log(ncells)), label = "$n\log(n)$")
 #   plt.loglog(ncells, allTimes, label = "full profile")
        
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)

    
    plt.xlabel("ncell values")
    plt.ylabel("time")
    plt.show()

    #pass in list of function names
   
    #be able to pick out functions by cumulative or within one specific function
    #split up example between setup and solve
    #start using sumatra for storing profile data
#    getFcnStats -> getValues needs runFunc
 #   getTuples(pointers) find tuples based on pointers
  #  getStatTuples() call pstats and convert
   # plotStats takes in getValues for tuples

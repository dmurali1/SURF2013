#file: profiling_functions.py

from fipy import Grid1D, CellVariable, TransientTerm, DiffusionTerm, Viewer
import cProfile
import pstats 
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import inspect


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

    def get_sorted_keys(self, ncell, sort_field="cumulative"):
        sorted_stats = self.get_stats(ncell).sort_stats(sort_field)
        return sorted_stats.fcn_list


    def get_time_for_function(self, function_key, ncell):
        return self.get_stats(ncell).stats[function_key][3]

    @staticmethod
    def get_key_from_function_pointer(function_pointer):
        return (inspect.getfile(function_pointer), inspect.getsourcelines(function_pointer)[1], function_pointer.func_name)

    def plot(self, keys):

        for key in keys:
            functionTimes = []
            for ncell in ncells:
                print ncell,
                functionTimes.append(get_time_for_function(key, ncell))
            plt.loglog(self.ncells, functionTimes, label = fuction_pointers.func_name)           

        allTimes = []
        runfunc_key = get_key_from_function_pointer(self.runfunc)
        for ncell in self.ncells:
            print ncell,
            allTimes.append(self.get_time_for_function(runfunc_key, ncell)  
        plt.loglog(self.ncells, allTimes, label = "full profile")        

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                   ncol=3, fancybox=True, shadow=True)




##file: profiling_functions.py
from fipy import Grid1D, CellVariable, TransientTerm, DiffusionTerm, Viewer
import cProfile
import pstats 
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import inspect
import matplotlib.gridspec as gridspec
from fipyprofile import FiPyProfile
import datetime
import time

class FiPyProfileTime(FiPyProfile):
    def __init__(self, runfunc, ncell, regenerate=False, funcString=None):
        self.runfunc = runfunc
        self.ncell = ncell
        self.regenerate = regenerate
        self.funcString = funcString
        if not os.path.exists(self.datafilestring()) or self.regenerate:
            print
            print 'generate data for ',ncell
            t0 = time.time()
            self.profile()
            print 'time taken ',time.time() - t0
            print

    def datafilestring(self):
        return "data/{funcString}{ncell}.stats".format(funcString=self.funcString, ncell=self.ncell)
	# now = datetime.datetime.now() 
        # year = now.year
        # month = now.month
        # day = now.day
        # hour = now.hour

        # dateString = "{month}-{day}-{year}_{hour}.stats".format(month=month, day=day, year=year, hour=hour)
        # return dateString
	#return str({now})[:16].replace(" ", "_")).stats.format(now=now)
	
    def profile(self):
        runFuncString = 'self.runfunc(ncell={ncell})'.format(ncell=self.ncell)
        cProfile.runctx(runFuncString, globals(), locals(), filename=self.datafilestring())
        
    def get_stats(self):
        return pstats.Stats(self.datafilestring())

    def get_sorted_keys(self, sort_field="cumulative"):
        sorted_stats = self.get_stats().sort_stats(sort_field)
        return sorted_stats.fcn_list

    
    def get_time_for_function(self, function_key, index=3):
        """index = 3 refers to cumulative time"""
        
        stats =  self.get_stats().stats
        if function_key in stats:
            return stats[function_key][index]
        else:
            return np.nan

    @staticmethod
    def get_key_from_function_pointer(function_pointer):
        return (inspect.getfile(function_pointer), inspect.getsourcelines(function_pointer)[1], function_pointer.func_name)

    def getIndex(self, field):
        sort_args = self.get_stats().get_sort_arg_defs()[field]
        return sort_args[0][0][0]

class ProfileViewer(object):
    def makelabel(self, key, shortLabel=True):
        if key[0] == '~':
            label = key[2]
        else:
            if shortLabel:
                fileName = os.path.split(key[0])[1]
            else:
                fileName = key[0]
            label = fileName + ": " + key[2]

        return r""+str(label).replace("_", "\_").replace("<", "$<$").replace(">", "$>$")

    def getIndex(self, profiler):
        sort_args = profilers[0].get_stats().get_sort_arg_defs()[field]
        return sort_args[0][0][0]

    def plot(self, profilers, keys, linetypes=None, labels=None, field="cumulative", ylabel=None):
        index = profilers[0].getIndex(field)
          
        fig = plt.figure(figsize=(8, 6))

        if not linetypes:
            linetypes = [None] * len(keys)

        if not labels:
            labels = [self.makelabel(k) for k in keys]

        ncells = np.array([p.ncell for p in profilers])

        for key, linetype, label in zip(keys, linetypes, labels):
            times = [p.get_time_for_function(key, index) for p in profilers]
            plt.loglog(ncells, times, linetype, label = label, lw=2)
            
        if ylabel:
            plt.ylabel(ylabel)
        else:
            plt.ylabel(sort_args[1])
        plt.xlabel(r"Number of Cells ($N$)")
      
        ncells = ncells[int(len(ncells) * (2. / 3.)):]
        multiplier = times[-1] / ncells[-1]**2
        plt.loglog(ncells, multiplier * ncells**2, label=r"$N^2$", lw=2)
        multiplier = times[-1] / (ncells[-1]*np.log(ncells[-1]))
        plt.loglog(ncells, multiplier * ncells*np.log(ncells),'b:', label=r"$N\log(N)$", lw=4)

        plt.legend(loc='lower right')

    def show(self):
        plt.legend(loc='lower right')
       # plt.show()
        plt.savefig("extremefill_time_danya.png")




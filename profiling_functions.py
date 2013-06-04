#file: profiling_functions.py

from fipy import Grid1D, CellVariable, TransientTerm, DiffusionTerm, Viewer
import cProfile
import pstats 
import os
import numpy as np
import matplotlib.pyplot as plt

def getProfileStats(importFile, ncell=100, regenerate=False):
    filename = "data/{importFile}{ncell}.stats".format(importFile=importFile, ncell=ncell)
    if not os.path.exists(filename) or regenerate:
        importFileString = 'importFile(ncell={ncell})'.format(ncell=ncell)
        cProfile.runctx(importFileString, globals(), locals(), filename=filename)
    return pstats.Stats(filename)
       
       
def getKey(statsDict, fcnName):
    for k in statsDict.keys():
        if fcnName in k[2]:
            return k


def getFcnStats(importFile, ncell=100, fcnName=None, regenerate=False):
    a  = getProfileStats(importFile, ncell, regenerate=regenerate)
    if fcnName:
        return a.stats[getKey(a.stats, fcnName)][3]
    else:
        a = a.sort_stats("cumulative")
        return a.stats[a.fcn_list[0]][3]


def plotStats(importFile, ncells, fcnName=None, regenerate=False):
  
    allTimes = []
    times = []
    for ncell in ncells:
        print ncell
    
        allTimes.append(getFcnStats(importFile, ncell=ncell, regenerate=regenerate))  
        times.append(getFcnStats(importFile, ncell=ncell, fcnName=fcnName, regenerate=regenerate))
    

    p1 = plt.loglog(ncells, allTimes)      
    plt.xlabel("ncell values")
    plt.ylabel("time")
    p2 = plt.loglog(ncells, times)
    plt.legend( (p1[0], p2[0]), ('Full Profile', fcnName) )
    plt.show()

def getProfileStats(importFile, nx=100, regenerate=False):
    import cProfile
    import os 
    filename = "data/{func_name}{nx}.stats".format(func_name=importFile.func_name, nx=nx)
    if not os.path.exists(filename) or regenerate:
        ## cProfile.run('{func_name}(nx={nx})'.format(func_name=importFile.func_name, nx=nx), filename=filename)
        cProfile.runctx('importFile(nx={nx})'.format(nx=nx), globals=globals(), locals=locals(), filename=filename)
    return pstats.Stats(filename)
       
       
def getKey(statsDict, fcnName):
    for k in statsDict.keys():
        if fcnName in k[2]:
            return k


def getFcnStats(importFile, nx=100, fcnName=None, regenerate=False):
    a  = getProfileStats(importFile, nx, regenerate=regenerate)
    if fcnName:
        return a.stats[getKey(a.stats, fcnName)][3]
    else:
        a = a.sort_stats("cumulative")
        return a.stats[a.fcn_list[0]][3]


def plotStats(importFile, fcnName=None, regenerate=False):
    import matplotlib.pyplot as plt
    import numpy as np

    step = 0
    while step < 1:
       nxs = np.array(logspace(1, 3, 100), dtype=int)
       allTimes = []
       times = []
       for nx in nxs:
            allTimes.append(getFcnStats(importFile, nx=nx, regenerate=regenerate))
            times.append(getFcnStats(importFile, nx=nx, fcnName=fcnName, regenerate=regenerate))
       step += 1
    
       p1 = plt.loglog(nxs, allTimes)
       p2 = plt.loglog(nxs, times)
       plt.xlabel("nx values")
       plt.ylabel("time")
       plt.legend( (p1[0], p2[0]), ('Full Profile', fcnName) )
       plt.show()

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

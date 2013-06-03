def getFcnStats(importFile, nx=100, fcnName=None, regenerate=False):
    a  = getProfileStats(importFile, nx, regenerate=regenerate)
    if fcnName:
        return a.stats[getKey(a.stats, fcnName)][3]
    else:
        a = a.sort_stats("cumulative")
        return a.stats[a.fcn_list[0]][3]

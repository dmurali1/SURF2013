def getKey(statsDict, fcnName):
    for k in statsDict.keys():
        if fcnName in k[2]:
            return k

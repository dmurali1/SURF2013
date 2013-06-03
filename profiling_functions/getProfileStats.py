def getProfileStats(importFile, nx=100, regenerate=False):
    print importFile.func_name
    import os 
    filename = "data/{func_name}{nx}.stats".format(func_name=importFile.func_name, nx=nx)
    if not os.path.exists(filename) or regenerate:
        ## cProfile.run('{func_name}(nx={nx})'.format(func_name=importFile.func_name, nx=nx), filename=filename)
        cProfile.runctx('importFile(nx={nx})'.format(nx=nx), globals=globals(), locals=locals(), filename=filename)
    return pstats.Stats(filename)
              

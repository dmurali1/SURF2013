from profiling_memory import MemoryViewer
from polyxtal import PolyxtalSimulation
from polyxtal import func
import numpy as np

ncells = np.array(np.logspace(1, 3, 25), dtype=int)
memoryViewer = MemoryViewer(ncells, PolyxtalSimulation.setup, func, (14, 17, 103, 106))
data = memoryViewer.generateData()

files = ["data/data0_{ncell}_polyxtal".format(ncell=n) for n in ncells]
memoryViewer.savedata(data, files)
data = memoryViewer.readdata(files)
memoryViewer.plot(data)




# from fipy.terms.term import Term

# ncells = np.array(np.logspace(1, 5, 5), dtype=int)
# memoryViewer2 = MemoryViewer(ncells, Term.solve, func, (209,))
# data = memoryViewer2.generateData()
# files = ["data/data0_{ncell}_solver".format(ncell=n) for n in ncells]
# memoryViewer2.savedata(data, files)
# data = memoryViewer.readdata(files)
# memoryViewer2.plot(data)


#change timestep to 1
#plot (1, 5, 10)
#plot before solver and after solver

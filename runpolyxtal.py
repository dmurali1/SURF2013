from profiling_memory import MemoryViewer
from polyxtal import PolyxtalSimulation, PolyxtalSimulationGmsh
from polyxtal import func, func2
import numpy as np
import matplotlib.pyplot as plt
from fipy.terms.term import Term


ncells = np.array(np.logspace(1, 6, 10), dtype=int)
lines = (21, 25, 111, 113)
memoryViewer4 = MemoryViewer(ncells, PolyxtalSimulationGmsh.setup, func2, lines)
#data4 = memoryViewer4.generateData()
files = ["data/data0_{ncell}_gmesh".format(ncell=n) for n in ncells]
#memoryViewer4.savedata(data4, files)
data4 = memoryViewer4.readdata(files)
#memoryViewer4.plot(data4)

ncells = np.array(np.logspace(1, 6, 10), dtype=int)
memoryViewer = MemoryViewer(ncells, PolyxtalSimulation.setup, func, lines)
#data = memoryViewer.generateData()
files = ["data/data0_{ncell}_polyxtal".format(ncell=n) for n in ncells]
#memoryViewer.savedata(data, files)
data = memoryViewer.readdata(files)
#memoryViewer.plot(data)

def plot(data, lines, ncells):
    
    memoryValues4 = np.array(data).swapaxes(0,1)
        
    for label, memory in zip(lines, memoryValues4):
        plt.loglog(ncells, memory, label=label)

    plt.xlabel("ncells")
    plt.ylabel("maximum memory values (MB)")
    
    plt.legend(loc="upper left")
    plt.savefig("polyxtal_gmesh.png")

def multiplot(data, data2, lines, ncells):

    memoryValues = np.array(data).swapaxes(0,1)
    memoryValues4 = np.array(data2).swapaxes(0,1)

    plt.loglog(ncells, memoryValues[0], "k", label="Total", lw=3)
    plt.loglog(ncells, memoryValues[1], "k", linestyle="dashdot", label="Base")
    plt.loglog(ncells, memoryValues[3], "k--", label="Setup")
    

    plt.loglog(ncells, memoryValues4[0], "r", label="Total (Gmsh)", lw=3)
    plt.loglog(ncells, memoryValues4[2], "r--", label="Setup (Gmsh)")
  

    plt.ylim(ymin=10.)
    plt.loglog(ncells, 500. * 8. * ncells / 1024. / 1024., "b:", label=r"500$\times N \times$float64", lw=2) 
    
    plt.xlabel("Number of Cells ($N$)")
    plt.ylabel("Memory (MB)")
    plt.legend(loc="upper left")
    plt.savefig("polyxtal_gmesh")
    
if __name__ == '__main__':
    multiplot(data, data4, lines, ncells)

# memoryViewer2 = MemoryViewer(ncells, Term.solve, func, (210,))
# #data2 = memoryViewer2.generateData()
# files2 = ["data/data0_{ncell}_solver".format(ncell=n) for n in ncells]
# #memoryViewer2.savedata(data2, files2)
# data2 = memoryViewer.readdata(files2)
# #memoryViewer2.plot(data2)

# from fipy.solvers.pysparse.pysparseSolver import PysparseSolver
# memoryViewer3 = MemoryViewer(ncells, PysparseSolver._solve_, func, (68, 75, 78))
# #data3 = memoryViewer3.generateData()
# #print "data3:" , data3
# files3 = ["data/data0_{ncell}_pysparse".format(ncell=n) for n in ncells]
# #memoryViewer3.savedata(data3, files3)
# data3 = memoryViewer3.readdata(files3)

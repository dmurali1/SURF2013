from profiling_memory import MemoryViewer
from polyxtal import PolyxtalSimulation
from polyxtal import func
import numpy as np
import matplotlib.pyplot as plt
from fipy.terms.term import Term


ncells = np.array(np.logspace(1, 6, 10), dtype=int)
memoryViewer = MemoryViewer(ncells, PolyxtalSimulation.setup, func, (14, 17, 102))
#data = memoryViewer.generateData()
files = ["data/data0_{ncell}_polyxtal".format(ncell=n) for n in ncells]
#memoryViewer.savedata(data, files)
data = memoryViewer.readdata(files)
#memoryViewer.plot(data)


memoryViewer2 = MemoryViewer(ncells, Term.solve, func, (209,))
#data2 = memoryViewer2.generateData()
files2 = ["data/data0_{ncell}_solver".format(ncell=n) for n in ncells]
#memoryViewer2.savedata(data, files2)
data2 = memoryViewer.readdata(files2)
#memoryViewer2.plot(data)

def multiplot(data, data2, datalines, data2line, ncells):
    """full profile for function run: [0], line profiler for function run: [-1]"""

    memoryValues = np.array(data).swapaxes(0,1)
    memoryValues2 = np.array(data2).swapaxes(0,1)

    plt.loglog(ncells, memoryValues[0], label="full profile", lw=2)
    plt.loglog(ncells, memoryValues2[-1], label="line profile: Term.solve: {line}".format(line=data2line), lw=2)
    for label, memory in zip(datalines, memoryValues[1:]):
        plt.loglog(ncells, memory, label="line profile: Polyxtal.setup: {line}".format(line=label), lw=2)
    
    
    ncells = ncells[int(len(ncells) * (3. / 4.)):]

    multiplier = memoryValues[0][-1] / ncells[-1]**2
    plt.loglog(ncells, multiplier * ncells**2, 'b--', label=r"$N^2$", lw=2)

    multiplier = memoryValues[0][-1] / (ncells[-1]*np.log(ncells[-1]))
    plt.loglog(ncells, multiplier * ncells*np.log(ncells), 'r--', label=r"$N\log(N)$", lw=2)

    multiplier = memoryValues[0][-1] / ncells[-1]
    plt.loglog(ncells, multiplier* ncells, "g--",label=r"$N$", lw=2)


    plt.xlabel("ncells")
    plt.ylabel("maximum memory values (MB)")
    plt.legend(loc="upper left")
    plt.savefig("polyxtal_bamesh_intvar_termsolve_scaled.png")

    
if __name__ == '__main__':
    multiplot(data, data2, [14, 17, 102], 209, ncells)


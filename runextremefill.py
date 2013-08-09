import argparse
import os
import numpy as np


parser = argparse.ArgumentParser(description='profile extremefill')
parser.add_argument('--filestring', type=str)
parser.add_argument('--inline', action="store_true")
parser.add_argument('--outputfile', type=str)
parser.add_argument('--regenerate', action="store_true")
args = parser.parse_args()

if args.inline:
    os.environ['FIPY_INLINE'] = ''


from profiling_memory import MemoryViewer
from polyxtal import PolyxtalSimulation, PolyxtalSimulationGmsh
from polyxtal import func, func2
from fipy.terms.term import Term
from plotting import plot
from extremefill2D.simulation2D import Simulation2D


class Simulation2DProfile(Simulation2D):
    def _run(self, ncell):
        self.run(totalSteps=2,
                 Nx=int(np.sqrt(ncell * 7.34)),
                 CFL=0.1,
                 sweeps=4,
                 tol=1e-10,
                 areaRatio=2 * 0.093,
                 solver_tol=1e-6,
                 dtMax=1.,
                 totalTime=5000.,
                 PRINT=False,
                 dt=0.01)
        
def runExtremefFill(ncell):
    Simulation2DProfile()._run(ncell)

ncells = np.array(np.logspace(2, 6, 25), dtype=int)
lines = (97, 105, 204, 215)
memoryViewer = MemoryViewer(ncells, Simulation2DProfile.run, runExtremefFill, lines)
files = ["data/{filestring}_{ncell}".format(filestring=args.filestring, ncell=n) for n in ncells]
if args.regenerate:
    data = memoryViewer.generateData()
    memoryViewer.savedata(data, files)
data = memoryViewer.readdata(files)

memoryValues = np.array(data).swapaxes(0,1)




datadict = {'base' : {'values' : memoryValues[1], 'label' : 'base', 'linecolor' : 'k', 'linetype' : 'dashdot'},
            'setup' : {'values' : memoryValues[3], 'label' : 'setup', 'linecolor' : 'k--', 'linetype' : 'dashed'},
            'total' : {'values' : memoryValues[0], 'label' : 'total', 'linecolor' : 'k', 'linetype' : 'solid'}}

plot(datadict, ncells, datafile=args.outputfile)

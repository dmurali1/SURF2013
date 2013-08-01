import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='profile extremefill')
parser.add_argument('--filestring', type=str)
parser.add_argument('--trilinos', action="store_true")
parser.add_argument('--outputfile', type=str)
parser.add_argument('--regenerate', action="store_true")
args = parser.parse_args()

if args.trilinos:
    os.environ['FIPY_SOLVERS'] = 'trilinos'

from fipyprofile import FiPyProfile
from profiling_functions import FiPyProfileTime
from polyxtal import PolyxtalSimulation, PolyxtalSimulationPysparseNoPrecon, PolyxtalSimulationTrilinosNoPrecon
from profiling_functions import ProfileViewer
        
ncells = np.array(np.logspace(2, 5, 10), dtype=int)
polyxtal = PolyxtalSimulationTrilinosNoPrecon()
profilers = [FiPyProfileTime(polyxtal.run, ncell, regenerate=True, funcString='polyxtal_trilinos_noPrecon1') for ncell in ncells]
runkey = profilers[0].get_key_from_function_pointer(polyxtal.run)
keys = [runkey,]
viewer = ProfileViewer()
field = "cumulative"


prof = profilers[0]
index = prof.getIndex(field)
runkey = prof.get_key_from_function_pointer(polyxtal.run)
times = [p.get_time_for_function(runkey, index) for p in profilers]

print "ncells:", ncells
print "times:", times
raw_input("Done.")

plt.loglog(ncells, times, 'r', label = 'Total', lw=2)
plt.show()


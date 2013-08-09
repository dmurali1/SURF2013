import numpy as np
from fipyprofile import FiPyProfile
from profiling_functions import FiPyProfileTime
from polyxtal import PolyxtalSimulation, PolyxtalSimulationPCG
import matplotlib.pyplot as plt
from fipy.solvers.pysparse.pysparseSolver import PysparseSolver 
from fipy.solvers.trilinos.trilinosSolver import TrilinosSolver
from fipy.solvers.trilinos.trilinosAztecOOSolver import TrilinosAztecOOSolver


ncells = np.array(np.logspace(2, 5, 10), dtype=int)
polyxtal = PolyxtalSimulation()
polyxtaltrilinos = PolyxtalSimulationPCG()

### With trilinos ###
profilers_trilinos = [FiPyProfileTime(polyxtaltrilinos, ncell, regenerate=False, funcString='polyxtal_trilinos_PCG_4') for ncell in ncells]
field = "cumulative"
prof = profilers_trilinos[0]

index = prof.getIndex(field)

runkey = prof.get_key_from_function_pointer(polyxtaltrilinos.run)
times = [p.get_time_for_function(runkey, index) for p in profilers_trilinos]
plt.loglog(ncells, times, 'r', label = 'Trilinos Total', lw=2)

solvekey = prof.get_key_from_function_pointer(TrilinosAztecOOSolver._solve_)
times = [p.get_time_for_function(solvekey, index) for p in profilers_trilinos]
plt.loglog(ncells, times, 'r--', label = ' Trilinos Solver', lw=2)


### With pysparse ###
profilers = [FiPyProfileTime(polyxtal, ncell, regenerate=False, funcString='polyxtal_pysparse_2') for ncell in ncells]
field = "cumulative"
prof = profilers[0]
for key in prof.get_stats().stats.keys():
    if "run" in key[2]:
        print key
index = prof.getIndex(field)
solvekey = prof.get_key_from_function_pointer(PysparseSolver._solve_)
times = [p.get_time_for_function(solvekey, index) for p in profilers]
plt.loglog(ncells, times, 'k--', label = 'Solver', lw=2)

#runkey = prof.get_key_from_function_pointer(polyxtal.run)
runkey = ('/users/ddm1/work/polyxtal.py', 112, 'run')
times = [p.get_time_for_function(runkey, index) for p in profilers]
print "times", times
plt.loglog(ncells, times, 'k', label = 'Total', lw=2)

plt.legend(loc="upper left")
plt.savefig("polyxtal_trilinos_PCG.png")

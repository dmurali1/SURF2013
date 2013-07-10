from profiling_functions import FiPyProfileTime
from polyxtal import PolyxtalSimulation
from fipyprofile import FiPyProfile
import numpy as np
from coupled1D import CoupledSimulation

ncells = np.array(np.logspace(1, 2, 2), dtype=int)
polyxtal = PolyxtalSimulation()
coupled = CoupledSimulation()
prof = FiPyProfileTime(coupled.run, ncells, regenerate=True)
keys = prof.get_sorted_keys(ncells[0], sort_field="cumulative")
prof.plot(keys[:5], "cumulative", doFullProfile=True)

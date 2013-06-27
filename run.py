from profiling_functions import FiPyProfileTime
from polyxtal import PolyxtalSimulation
from fipyprofile import FiPyProfile
import numpy as np
from coupled1D import CoupledSimulation

ncells = np.array(np.logspace(1, 5, 25), dtype=int)
polyxtal = PolyxtalSimulation()
coupled = CoupledSimulation()
prof = FiPyProfileTime(coupled.setup, ncells, regenerate=True)
keys = prof.get_sorted_keys(ncells[-1], sort_field="time")
prof.plot(keys[:0], "time", doFullProfile=True)


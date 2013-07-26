from fipyprofile import FiPyProfile
from profiling_functions import FiPyProfileTime
from polyxtal import PolyxtalSimulation, PolyxtalSimulationGmsh
import numpy as np

ncells = np.array(np.logspace(1, 6, 10), dtype=int)
polyxtal = PolyxtalSimulationGmsh()
prof = FiPyProfileTime(polyxtal.run, ncells, "data/polyxtalgmsh.run", regenerate=True)
keys = prof.get_sorted_keys(ncells[0], sort_field="cumulative")
prof.plot(keys[:2], "cumulative", doFullProfile=True)

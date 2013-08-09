import os

os.environ['FIPY_INLINE'] = ''

from fipyprofile import FiPyProfile
from profiling_functions import FiPyProfileTime
from polyxtal import PolyxtalSimulation
import numpy as np
from extremefill2D.simulation2D import Simulation2D
from profiling_functions import ProfileViewer
from fipy.solvers.pysparse.pysparseSolver import PysparseSolver 
class Simulation2DProfile(Simulation2D):
    def _run(self, ncell):
        self.run(totalSteps=10,
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
        
ncells = np.array(np.logspace(2, 6, 20), dtype=int)
polyxtal = PolyxtalSimulationGmsh()
#profilers = [FiPyProfileTime(sim2D._run, ncell, regenerate=True, funcString='extremefill2-') for ncell in ncells]
inlineprofilers = [FiPyProfileTime(polyxtal.run, ncell, regenerate=True, funcString='polyxtal-inline-gmsh-') for ncell in ncells]

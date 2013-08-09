#GENERATE DATA FOR POLYXTAL
      #WITH INLINE
      #WITHOUT INLINE 
#GENERATE DATA FOR EXTREMEFILL
      #WITH GMSH
      #WITHOUT GMSH

#MAKE 4 SEPERATE PLOTS (TIME AND MEMORY FOR EACH)
import os
import sys
from profiling_functions import ProfileViewer

if sys.argv[1] == 'extremefill':
    import os
    import sys

    funcString = 'final-extremefill-'

    if len(sys.argv) > 1 and sys.argv[2] == 'inline':
        os.environ['FIPY_INLINE'] = ''
  #      print'extremefill inline'
        funcString += 'inline-'

    from fipyprofile import FiPyProfile
    from profiling_functions import FiPyProfileTime
    from polyxtal import PolyxtalSimulation
    import numpy as np
    from extremefill2D.simulation2D import Simulation2D
    from profiling_functions import ProfileViewer
    from fipy.solvers.pysparse.pysparseSolver import PysparseSolver 
    from polyxtal import PolyxtalSimulation
    from polyxtal import PolyxtalSimulationGmsh 
    from profiling_functions import ProfileViewer



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

                
    ncells = np.array(np.logspace(2, 5, 10), dtype=int)
    sim2D = Simulation2DProfile()
    profilers = [FiPyProfileTime(sim2D._run, ncell, regenerate=True, funcString=funcString) for ncell in ncells]
   

###########################################

if sys.argv[1] == 'polyxtal':

    from fipyprofile import FiPyProfile
    from profiling_functions import FiPyProfileTime
    from polyxtal import PolyxtalSimulation
    import numpy as np
    from extremefill2D.simulation2D import Simulation2D
    from profiling_functions import ProfileViewer
    from fipy.solvers.pysparse.pysparseSolver import PysparseSolver 
    from polyxtal import PolyxtalSimulation
    from polyxtal import PolyxtalSimulationGmsh 
    from profiling_functions import ProfileViewer
    funcString = 'final-polyxtal-'
    polyxtal = PolyxtalSimulation()

    if len(sys.argv) > 1 and sys.argv[2] == 'gmsh':
        funcString += 'gmsh-'
        polyxtal = PolyxtalSimulationGmsh()
  #      print 'polyxtal gmsh'
   

        
    ncells = np.array(np.logspace(2, 5, 10), dtype=int)
    profilers = [FiPyProfileTime(polyxtal.run, ncell, regenerate=True, funcString=funcString) for ncell in ncells]
  
##############################time to plot###################################
from fipyprofile import FiPyProfile
from profiling_functions import FiPyProfileTime
from polyxtal import PolyxtalSimulation
import numpy as np
from extremefill2D.simulation2D import Simulation2D
from profiling_functions import ProfileViewer
from fipy.solvers.pysparse.pysparseSolver import PysparseSolver 
from polyxtal import PolyxtalSimulation
from polyxtal import PolyxtalSimulationGmsh 
from profiling_functions import ProfileViewer
 
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

sim2D= Simulation2DProfile()
polyxtal = PolyxtalSimulationGmsh()

profilers_e= [FiPyProfileTime(sim2D.run, ncell, regenerate=False, funcString='final-extremefill-') for ncell in ncells]
profilers_ei = [FiPyProfileTime(sim2D.run, ncell, regenerate=False, funcString='final-extremefill-inline-') for ncell in ncells]
profilers_p = [FiPyProfileTime(polyxtal.run, ncell, regenerate=False, funcString='final-polyxtal-') for ncell in ncells]
profilers_pg = [FiPyProfileTime(polyxtal.run, ncell, regenerate=False, funcString='final-polyxtal-gmsh-') for ncell in ncells]

viewer = ProfileViewer()
field = "cumulative"
###PLOT 1 - Extremefill Speed #########
#solver and total for inline and not inline
import matplotlib.pyplot as plt

prof_e = profilers_e[0]
index = prof_e.getIndex(field)
solvekey = prof_e.get_key_from_function_pointer(PysparseSolver._solve_)
times = [p.get_time_for_function(solvekey, index) for p in profilers_e]
plt.loglog(ncells, times, 'r', label = 'Solver', lw=2)

index = prof_e.getIndex(field)
runkey = prof_e.get_key_from_function_pointer(sim2D.run)
times = [p.get_time_for_function(runkey, index) for p in profilers_e]
plt.loglog(ncells, times, 'k', label = 'Total', lw=2)

prof_ei = profilers_ei[0]
index = prof_ei.getIndex(field)
solvekey = prof_ei.get_key_from_function_pointer(PysparseSolver._solve_)
times = [p.get_time_for_function(solvekey, index) for p in profilers_ei]
plt.loglog(ncells, times, 'r--', label = 'Solver (inline)', lw=2)

index = prof_ei.getIndex(field)
runkey = prof_ei.get_key_from_function_pointer(sim2D.run)
times = [p.get_time_for_function(runkey, index) for p in profilers_ei]
plt.loglog(ncells, times, 'k--', label = 'Total (inline)', lw=2)

viewer.show1()
plt.close()
###PLOT 2 - Extremefill Memory #########

###PLOT 3 - Polyxtal Speed #########

viewer = ProfileViewer()
field = "cumulative"
import matplotlib.pyplot as plt2

prof_p = profilers_p[0]
index = prof_p.getIndex(field)
solvekey = prof_p.get_key_from_function_pointer(PysparseSolver._solve_)
times = [p.get_time_for_function(solvekey, index) for p in profilers_p]
plt2.loglog(ncells, times, 'r', label = 'Solver', lw=2)

index = prof_p.getIndex(field)
runkey = prof_p.get_key_from_function_pointer(polyxtal.run)
times = [p.get_time_for_function(runkey, index) for p in profilers_p]
plt2.loglog(ncells, times, 'k', label = 'Total', lw=2)

prof_pg = profilers_pg[0]
index = prof_pg.getIndex(field)
solvekey = prof_ei.get_key_from_function_pointer(PysparseSolver._solve_)
times = [p.get_time_for_function(solvekey, index) for p in profilers_pg]
plt2.loglog(ncells, times, 'r--', label = 'Solver (Gmsh)', lw=2)

index = prof_pg.getIndex(field)
runkey = prof_pg.get_key_from_function_pointer(polyxtal.run)
times = [p.get_time_for_function(runkey, index) for p in profilers_pg]
plt2.loglog(ncells, times, 'k--', label = 'Total (Gmsh)', lw=2)

viewer.show2()
###PLOT 4 - Polyxtal Memory  #########

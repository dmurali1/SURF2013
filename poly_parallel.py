import os

os.environ['FIPY_SOLVERS'] = 'trilinos'
#os.environ['FIPY_VERBOSE_SOLVER'] = ''

from polyxtal import PolyxtalSimulationTrilinosJacobiGmsh
def f(ncell):
    PolyxtalSimulationTrilinosJacobiGmsh(2).run(ncell)
f(100000)

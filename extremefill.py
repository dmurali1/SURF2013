import os
import shutil


from extremefill2D.simulation2D import Simulation2D

simulation = Simulation2D()
simulation.run(totalSteps=5,
               Nx=300,
               CFL=0.1,
               sweeps=30,
               tol=1e-1,
               areaRatio=2 * 0.093,
               dtMax=100.,
               totalTime=5000.,
               PRINT=True)
    

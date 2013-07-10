#file: polyxtal.py

from fipy import *
import numpy as np
from simulation import Simulation
from memory_profiler import profile
import gc
class PolyxtalSimulation(Simulation):

   # @profile
    def setup(self, ncell):

        dx = dy = 0.025
        nx = ny = int(np.sqrt(ncell))
        mesh = Grid2D(dx=dx, dy=dy, nx=nx, ny=ny)

        dt = 5e-4

        phase = CellVariable(name=r'$\phi$', mesh=mesh, hasOld=True)

        dT = CellVariable(name=r'$\Delta T$', mesh=mesh, hasOld=True)

        theta = ModularVariable(name=r'$\theta$', mesh=mesh, hasOld=True)
        theta.value = -numerix.pi + 0.0001


        DT = 2.25
        q = Variable(0.)
        T_0 = -0.1
        heatEq = (TransientTerm()
                  == DiffusionTerm(DT)
                  + (phase - phase.old) / dt
                  + q * T_0 - ImplicitSourceTerm(q))

        alpha = 0.015
        c = 0.02
        N = 4.
        psi = theta.arithmeticFaceValue + numerix.arctan2(phase.faceGrad[1], 
                                                          phase.faceGrad[0])
        Phi = numerix.tan(N * psi / 2)
        PhiSq = Phi**2
        beta = (1. - PhiSq) / (1. + PhiSq)
        DbetaDpsi = -N * 2 * Phi / (1 + PhiSq)
        Ddia = (1.+ c * beta)
        Doff = c * DbetaDpsi
        I0 = Variable(value=((1,0), (0,1)))
        I1 = Variable(value=((0,-1), (1,0)))
        D = alpha**2 * Ddia * (Ddia * I0 + Doff * I1)

        tau_phase = 3e-4
        kappa1 = 0.9
        kappa2 = 20.
        epsilon = 0.008
        s = 0.01
        thetaMag = theta.grad.mag
        phaseEq = (TransientTerm(tau_phase)
                   == DiffusionTerm(D)
                   + ImplicitSourceTerm((phase - 0.5 - kappa1 / numerix.pi * numerix.arctan(kappa2 * dT))
                                        * (1 - phase)
                                        - (2 * s + epsilon**2 * thetaMag) * thetaMag))

        tau_theta = 3e-3
        mu = 1e3
        gamma = 1e3
        thetaSmallValue = 1e-6
        phaseMod = phase + ( phase < thetaSmallValue ) * thetaSmallValue
        beta_theta = 1e5
        expo = epsilon * beta_theta * theta.grad.mag
        expo = (expo < 100.) * (expo - 100.) + 100.
        Pfunc = 1. + numerix.exp(-expo) * (mu / epsilon - 1.)
        gradMagTheta = theta.faceGrad.mag
        eps = 1. / gamma / 10.
        gradMagTheta += (gradMagTheta < eps) * eps
        IGamma = (gradMagTheta > 1. / gamma) * (1 / gradMagTheta - gamma) + gamma
        v_theta = phase.arithmeticFaceValue * (s * IGamma + epsilon**2)
        D_theta = phase.arithmeticFaceValue**2 * (s * IGamma + epsilon**2)

        thetaEq = (TransientTerm(tau_theta * phaseMod**2 * Pfunc) 
                   == DiffusionTerm(D_theta)
                   + (D_theta * (theta.faceGrad - theta.faceGradNoMod)).divergence)

        x, y = mesh.cellCenters
        numSeeds = 10
        numerix.random.seed(12345)
        for Cx, Cy, orientation in numerix.random.random([numSeeds, 3]):
            radius = dx * 5.
            seed = ((x - Cx * nx * dx)**2 + (y - Cy * ny * dy)**2) < radius**2
            phase[seed] = 1.
            theta[seed] = numerix.pi * (2 * orientation - 1)

        dT.setValue(-0.5)

        total_time = 2.

        elapsed = 0.
        save_interval = 0.002
        save_at = save_interval

        self.variables = (theta, phase, dT)
        self.eqns = (thetaEq, phaseEq, heatEq)
        self.q = q
        self.dt = dt
        self.elapsed = elapsed
        for step in range(10):
          
            self.time_step()
            
            


    def run(self, ncell=200**2):
        self.setup(ncell)
        self.continue_steps()
        
    def time_step(self):
        if self.elapsed > 0.3:
            self.q.value = 100
        for v in self.variables:
            v.updateOld()

        for v, e in zip(self.variables, self.eqns):
            e.solve(v, dt=self.dt)
        self.elapsed += self.dt


def func(ncell):
    polyxtal = PolyxtalSimulation()
    polyxtal.run(ncell)   
   
if __name__ == '__main__':
    from memory_profiler import LineProfiler
    prof = LineProfiler()
    func()
    print prof.code_map

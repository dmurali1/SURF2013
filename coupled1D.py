from fipy import Grid1D, CellVariable, TransientTerm, DiffusionTerm, Viewer
from simulation import Simulation

class CoupledSimulation(Simulation):


    def setup(self, ncell):
        m = Grid1D(nx=ncell, Lx=1.)


        v = CellVariable(mesh=m, hasOld=True, value=[[0.5], [0.5]], elementshape=(2,))

        v.constrain([[0], [1]], m.facesLeft)
        v.constrain([[1], [0]], m.facesRight)

        eqn = TransientTerm([[1,0], [0,1]]) == DiffusionTerm([[[0.01, -1], [1, 0.01]]])

        self.v = v
        self.eqn = eqn
        for step in range(2):
            self.time_step()

 


    def time_step(self):
        self.v.updateOld()
        self.eqn.solve(var=self.v, dt=1.e-3)
       

    def run(self, ncell=100):
        self.setup(ncell)
        self.continue_steps()



if __name__ == '__main__':
    coupled = CoupledSimulation()
    coupled.run()


                    
 

#File Name: diffusion_coupled.py
#FiPy example for practice
from fipy import Grid1D, CellVariable, TransientTerm, DiffusionTerm, Viewer
import cProfile
import pstats

factor = 0 
for i in range(2,10,2):
    factor = i

def Coupled():
    m = Grid1D(nx=100*factor, Lx=1.)
    print m
    v0 = CellVariable(mesh=m, hasOld=True, value=0.5)
    v1 = CellVariable(mesh=m, hasOld=True, value=0.5)
    
    v0.constrain(0, m.facesLeft)
    v0.constrain(1, m.facesRight)
    
    eq0 = TransientTerm() == DiffusionTerm(coeff=0.01) - v1.faceGrad.divergence
    eq1 = TransientTerm() == v0.faceGrad.divergence + DiffusionTerm(coeff=0.01)
    
    vi = Viewer((v0, v1))
    
    for t in range(100):
        v0.updateOld()
        v1.updateOld()
        res0 = res1 = 1e100
        while max(res0, res1) > 0.1:
            res0 = eq0.sweep(var=v0, dt=1e-5)
            res1 = eq1.sweep(var=v1, dt=1e-5)
       # if t % 10 == 0:
           # vi.plot()
                
    v0.value = 0.5
    v1.value = 0.5
                
    eqn0 = TransientTerm(var=v0) == DiffusionTerm(0.01, var=v0) - DiffusionTerm(1, var=v1)
    eqn1 = TransientTerm(var=v1) == DiffusionTerm(1, var=v0) + DiffusionTerm(0.01, var=v1)
                
    eqn = eqn0 & eqn1
                
    for t in range(1):
        v0.updateOld()
        v1.updateOld()
        eqn.solve(dt=1.e-3)
     #   vi.plot()
                    
    v = CellVariable(mesh=m, hasOld=True, value=[[0.5], [0.5]], elementshape=(2,))
                    
    v.constrain([[0], [1]], m.facesLeft)
    v.constrain([[1], [0]], m.facesRight)
                    
    eqn = TransientTerm([[1,0], [0,1]]) == DiffusionTerm([[[0.01, -1], [1, 0.01]]])
                    
    vi = Viewer((v[0], v[1]))
                    
    for t in range(1):
        v.updateOld()
        eqn.solve(var=v, dt=1.e-3)
       # vi.plot()

def main():

    filename = "tmp.stats"
    cProfile.run('Coupled()', filename=filename)
    p = pstats.Stats(filename)
    p.strip_dirs().sort_stats("cumulative").print_stats(20)



#f = open("tmp.txt", "r")
#line = f.readline()

#for line in range(10):
#    print line



main()

def Coupled(nx=100):

    m = Grid1D(nx=nx, Lx=1.)

           
    v = CellVariable(mesh=m, hasOld=True, value=[[0.5], [0.5]], elementshape=(2,))
                    
    v.constrain([[0], [1]], m.facesLeft)
    v.constrain([[1], [0]], m.facesRight)
                    
    eqn = TransientTerm([[1,0], [0,1]]) == DiffusionTerm([[[0.01, -1], [1, 0.01]]])
                    
    for t in range(10):
        v.updateOld()
        eqn.solve(var=v, dt=1.e-3)
       

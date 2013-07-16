#!/usr/bin/env python

## -*-Pyth-*-
 # ########################################################################
 # FiPy - a finite volume PDE solver in Python
 # 
 # Author: Jonathan Guyer <guyer@nist.gov>
 #   mail: NIST
 #    www: <http://www.ctcms.nist.gov/fipy/>
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are 
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 # 
 # ########################################################################
 ##

from fipy import Grid1D
from fipy.tools import numerix
from fipy.viewers import Viewer

from solar.device import Device
from solar.impurities import Donor, Acceptor
from solar.materials import Si, Vacuum
from solar.contacts import OhmicContact
from solar.traps import ShockleyReadHallTrap
from solar.lights import AM1_5
from solar.parsimoniousIterator import ParsimoniousIterator

import time

# Construct a 1D mesh with compressed cells at the pn-junction and at the
# contacts

start_time = time.time()

n_thickness = 1e-6 # m
p_thickness = 149e-6 # m
grid_resolution = 5e-8 # m

compression_factor = 0.8
compression_count = 10

compressed_dx = grid_resolution * compression_factor**numerix.arange(compression_count)
compressed_length = compressed_dx.sum()
compressed_dx = list(compressed_dx)

n_uncompressed_thickness = n_thickness - 2 * compressed_length
n_dx = n_uncompressed_thickness / round(n_uncompressed_thickness / grid_resolution)
n_dx = compressed_dx[::-1] + [n_dx] * int(n_uncompressed_thickness / n_dx) + compressed_dx

p_uncompressed_thickness = p_thickness - 2 * compressed_length
p_dx = p_uncompressed_thickness / round(p_uncompressed_thickness / grid_resolution)
p_dx = compressed_dx[::-1] + [p_dx] * int(p_uncompressed_thickness / p_dx + 0.5) + compressed_dx

mesh = Grid1D(dx=n_dx + p_dx)

# define the n-Si/p-Si junction on the mesh

x = mesh.cellCenters[0]

ntype = x < n_thickness
ptype = x >= n_thickness
vacuum = ~(ntype | ptype)

nsi_psi = (Si() * ntype + Si() * ptype + Vacuum() * vacuum)

nFaces = mesh.facesLeft
pFaces = mesh.facesRight
illuminatedFaces = mesh.facesLeft

nContact = OhmicContact(faces=nFaces)
pContact = OhmicContact(faces=pFaces)

diode = Device(mesh=mesh, 
               temperature=300, # K
               material=nsi_psi, 
               dopants=(Donor(concentration=1e22 * ntype, # m**-3"
                              ionizationEnergy=-1.), # eV
                        Acceptor(concentration=1e24 * ptype, # m**-3
                                 ionizationEnergy=-1.)), # eV
               traps=(ShockleyReadHallTrap(recombinationLevel=0, # eV
                                           electronMinimumLifetime=100e-6, # s
                                           holeMinimumLifetime=100e-6),), # s
               contacts=(pContact, nContact))

# initial calculations at short circuit
nContact.bias.value = 0. # V
pContact.bias.value = 0. # V

# solve in dark and then illuminate
diode.solve(solver=None, sweeps=5, outer_tol=1e4)

# shine the solar spectrum from left to right
light = AM1_5(orientation=[[1]], 
              faces=illuminatedFaces)
              
# sample the light source from 300 nm to 1 um at 10 nm intervals
diode.illuminate(light(wavelength=numerix.arange(300e-9, 1000e-9, 10e-9))) # m
 
# viewer = Viewer(vars=(diode.Ec, diode.Efn, diode.Efp, diode.Ev))
# npViewer = Viewer(vars=(diode.n, diode.p), log=True)
# 
# def view():
#     viewer.plot()
#     npViewer.plot()
    
# calculate the current-voltage characteristic by applying 0 V to 0.9 V to the n contact
# writing the intermediate results to the file JV.txt
JV = diode.JV(contact=nContact, 
              biases=ParsimoniousIterator(start=-0.2, stop=0.5, num=20), # V
              path="JVb.txt",
              sweeps=5, outer_tol=1e-4, currentContinuity=1.)

# calculate the open circuit voltage, based on the current-voltage curve just
# calculated
Voc = diode.Voc(contact=nContact, JV=JV)

print "Voc = ", Voc

# calculate the maximum power voltage, based on the current-voltage curve just
# calculated
Vmax = diode.Vmax(contact=nContact, JV=JV, Vtol=0.01, Ptol=0.01)

print "Vmax = ", Vmax

elapsed_time = time.time() - start_time

print elapsed_time

raw_input("done")
                            

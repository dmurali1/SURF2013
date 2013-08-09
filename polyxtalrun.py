import argparse
import os

parser = argparse.ArgumentParser(description='profile polyxtal')
parser.add_argument('--verbose', action="store_true")
parser.add_argument('--trilinos', action="store_true")
parser.add_argument('--no_precon', action="store_true")
parser.add_argument('--precon')
parser.add_argument('--steps', type=int, default=10)
args = parser.parse_args()

if args.verbose:
    os.environ['FIPY_VERBOSE_SOLVER'] = "verbose"

from polyxtal import PolyxtalSimulationTrilinos, PolyxtalSimulationPysparse, PolyxtalSimulationTrilinosNoPrecon, PolyxtalSimulationPysparseNoPrecon, PolyxtalSimulationTrilinosJacobi
if not args.no_precon:
    if args.trilinos:
        c = PolyxtalSimulationTrilinos
    else:
        c = PolyxtalSimulationPysparse
else:
    if args.trilinos:
        c = PolyxtalSimulationTrilinosNoPrecon
    else:
        c = PolyxtalSimulationPysparseNoPrecon

if args.precon == 'jacobi':
    c = PolyxtalSimulationTrilinosJacobi

c(steps=args.steps).run(100000)





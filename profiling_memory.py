#make a memory class 
#take memory profiler decorating fuction and put it in class
#have ability to put decorator on function passed in
from fipyprofile import FiPyProfile
from memory_profiler import LineProfiler


class FiPyProfileMemory(FiPyProfile):

    def profile(self, ncell):
        prof = LineProfiler()
        prof(self.runfunc)(ncell)
        self.code_map = prof.code_map 

if __name__ == '__main__':
    from polyxtal import PolyxtalSimulation
    polyxtal = PolyxtalSimulation()
    memory = FiPyProfileMemory(polyxtal.setup, "run", [200], True)
    print memory.code_map

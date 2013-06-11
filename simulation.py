
class Simulation:

    def setup(self, ncell):
        pass

    def run(self, ncell=100):
        pass

    def continue_steps(self):
        for t in range(10):
            self.time_step()

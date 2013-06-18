from fipy import Grid1D, CellVariable, TransientTerm, DiffusionTerm, Viewer
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import inspect
import matplotlib.gridspec as gridspec


class FiPyProfile(object):
    def __init__(self, runfunc, funcString, ncells, regenerate=False):
        self.runfunc = runfunc
        self.ncells = ncells
        self.regenerate = regenerate
        self.funcString = funcString
        for ncell in ncells:
            if not os.path.exists(self.datafilestring(ncell)) or self.regenerate:
                self.profile(ncell)

    def datafilestring(self, ncell):
        return "{funcString}{ncell}.stats".format(funcString=self.funcString, ncell=ncell)

    def profile(self, ncell):
        pass

    def get_stats(self, ncell):
        pass

    def get_sorted_keys(self, ncell):
        return sorted_stats.fcn_list

    def plot(self, keys):

        fig = plt.figure()
        gs = gridspec.GridSpec(2,1)
        ax1 = plt.subplot(gs[1, :-1])
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, ncol=1, mode="wrap", borderaxespad=0., prop={'size': 12})
        gs.tight_layout(fig, rect=[0,0,1,1])

import numpy as np
import matplotlib.pyplot as plt

def plot(datadict, ncells, datafile='out.png'):
    
   
    for k in datadict.keys():
        d = datadict[k]
        plt.loglog(ncells, d['values'], d['linecolor'], label=d['label'], linestyle=d['linetype'], lw=2)
    
    plt.ylim(ymin=10.)
    plt.loglog(ncells, 500. * 8. * ncells / 1024. / 1024., "b:", label=r"500$\times N \times$float64", lw=2) 
    
    # plt.loglog(ncells, memoryValues[0], "k", label=labels[0], lw=2)
    # plt.loglog(ncells, memoryValues[1], "k", linestyle="dotdash", label=labels[1])
    # plt.loglog(ncells, memoryValues[3], label=labels[2])
   

    plt.xlabel("Number of Cells ($N$)")
    plt.ylabel("Memory (MB)")
    
    plt.legend(loc="upper left")
    plt.savefig(datafile)

def multiplot(data, data2, datalines, data2lines, ncells):

    memoryValues = np.array(data).swapaxes(0,1)
    memoryValues4 = np.array(data2).swapaxes(0,1)

    plt.loglog(ncells, memoryValues[0], label="Total")
    plt.loglog(ncells, memoryValues[1], label="Base")
    plt.loglog(ncells, memoryValues[4], label="After Solve")

    #plt.loglog(ncells, memoryValues4[0], label="Total Gmsh Memory", lw=2)
    plt.loglog(ncells, memoryValues4[2], label="After Gmsh Mesh", lw=2)
  

    plt.ylim(ymin=10.)
    plt.loglog(ncells, 500. * 8. * ncells / 1024. / 1024., "k--", label=r"500$\times N \times$float64") 
    
    plt.xlabel("$N$")
    plt.ylabel("Maximum Memory Values (MB)")
    plt.legend(loc="upper left")
    plt.savefig("polyxtal_gmesh")

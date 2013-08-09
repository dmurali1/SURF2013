def plot(data, lines, ncells, datafile='out.png'):
    
    memoryValues4 = np.array(data).swapaxes(0,1)
        
    for label, memory in zip(lines, memoryValues4):
        plt.loglog(ncells, memory, label=label)

    plt.xlabel("ncells")
    plt.ylabel("maximum memory values (MB)")
    
    plt.legend(loc="upper left")
    plt.savefig('out.png')

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

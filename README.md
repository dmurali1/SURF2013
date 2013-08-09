## SURF 2013 ##

# Project Description #

This project was on creating speed and memory profiling tools to analyze and optimize FiPy. FiPy is a partial differential equation (PDE) solver that uses the Finite Volume Method to solve PDEs. FiPy is written in the scripting language Python because Python is a very intutive and user-friendly language with many numerical computing packages which  make implementing PDEs easier. 

The problem I looked at this summer was to create profiling tools to quantitatively measure how much time and memory was being used by FiPy. By measuring these resources, we could locate any time inefficient or memory wasteful algorithms within FiPy and try and optimize those algorithms and improve this program. By creating a more optimal version of FiPy we can use it to solve bigger and more complicated problems that can be very helpful and save lots of time and resources for the scientific community. 

# Preliminary Things #

Both our speed and memory profilers were based off of existing python profilers. The speed profiler utilized the python package cprofile, and the memory profiler used the python package memory_profile. The links for both of these are below: 
cprofile: http://docs.python.org/2/library/profile.html
memory_profile: https://pypi.python.org/pypi/memory_profiler

We also used the time profilers runsnakerun to get a greater understanding of how different functions interacted with one another, and to learn what functions called what other functions within FiPy. The link for runsnakerun is below:

runsnake: http://www.vrplumber.com/programming/runsnakerun/

For all of the preliminary installations that were required to set up the profilers, please see the requirements.txt file. 

# Project Methodology #

We began by working on the speed profiler. We used the cprofile package to do the actual timing of functions but we also added the option to time our functions based on the number of cells (ncells) that were created in the mesh which we used to solve the PDE. We could also specify function pointers of specific functions we wanted to profile. All of the data we collected was cached, and we could use the cached data to create plots of the full profile against any specific functions we profiled, or plots of the top worst performing functions. 

Creating the memory profilers was much harder because we had to apply a function decorator to any function we had to profile. We got around this by creating a wrapper function. We also had a function that allowed you to pass in a line number and get the amount of memory that line of code took up. Just like the speed profiler, all the data was cached and there was the option to plot the data. The profiler was run in multiple processes in order to get reproducible results. 

Automating the Code:
There are two files, the first file runs the second under different conditions. The result is four sets of data being created: extremefill with and without inline, and polyxtal with and without gmsh. Then, once all the data has been created and stored, four graphs are created to detail the time and memory consumption of both simulations, and display the performance of multiple functions within the simulations. This was completed for the speed profiler but not yet for the memory profiler. 

# Post Presentation #

The following link has the slides of the presentation I gave at the NIST SURF colloquium: 
http://www.slideshare.net/dmurali2/danya-murali-presentation-1

The poster for this project can also be found here: 
http://www.slideshare.net/dmurali2/poster-final-25095523


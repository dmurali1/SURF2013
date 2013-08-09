## SURF 2013 

# Project Description 

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

We began by 

# Post Presentation #

The following link has the slides of the presentation I gave at the NIST SURF colloquium: 
http://www.slideshare.net/dmurali2/danya-murali-presentation-1

The poster for this project can also be found here: 
http://www.slideshare.net/dmurali2/poster-final-25095523


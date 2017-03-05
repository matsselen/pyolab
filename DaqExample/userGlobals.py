"""
Files starting with the name "user", like this one, are provided 
so that users can create their own analysis jobs.

This file is a handy place for the user to put any global variables
that she might need. Not that global variables are a great idea, mind you,
but its something Mats understands.   

"""

class U(object):

    analUserCalls = 0           # how many times analUserLoop() has been called
                                # (just for example - not needed in your own code)


    lastDataPrinted = 0         # keeping track of what we have already printed
    sensNum = 0                 # will be used to store the sensor numnber we want to print


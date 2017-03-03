"""
This is a cheap (and probably naive) trick to allow us to separate the 
user code from the analysis code. We basically create an instance
of this class in the main user code, and in so doing we tell the 
analysis code which user methods to call during the analysis. 

The class is instantiated in the "main" routine of your code 
(which is called userExample.py in this example), thus:

    anal = A(analUserStart, analUserEnd, analUserLoop)

where analUserStart(), analUserEnd(), analUserLoop() are defined by you,
and currently have examples living in "userMethods.py"

"""

class A(object):
    a = ''
    def __init__(self,an1,an2,an3):
        print "creating instance of A"
        self.analStart = an1
        self.analEnd   = an2
        self.analLoop  = an3
        A.a = self






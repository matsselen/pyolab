"""
This is a cheap (and probably naive) trick to allow us to separate the 
user code from the analysis code. We basically instantiate an instance
of this class in the main user code, and in so doing we tell the 
analysis code which user methods to call during the analysis. 

"""

class A(object):
    a = ''
    def __init__(self,an1,an2,an3):
        print "creating instance of A"
        self.analStart = an1
        self.analEnd   = an2
        self.analLoop  = an3
        A.a = self






#
# This file is part of PyOLab. https://github.com/matsselen/pyolab
# (C) 2017 Mats Selen <mats.selen@gmail.com>
#
# SPDX-License-Identifier:    BSD-3-Clause
# (https://opensource.org/licenses/BSD-3-Clause)
#

"""
Files starting with the name "user", like this one, are provided 
so that users can create their own analysis jobs.

This file is a handy place for the user to put any global variables
that she might need. Not that global variables are a great idea, mind you,
but its something Mats understands.   

"""

class U(object):

    lastRecord = 0         # keeping track of what we have already printed

    analUserCalls = 0      # how many times analUserLoop() has been called
                           # (just for example - not needed in your own code)

    payload = ''
    selection = ''
    
    # command record information keyed by command number
    promptDict = {
        0x14 : ['payload: (none)',''],
        0x20 : ['payload: (none)',''],
        0x21 : ['payload: (none)',''],
        0x22 : ['remote, Npr, Npr*[sens,keyval]',''],
        0x23 : ['remote','1'],
        0x24 : ['remote, Npr, Npr*[sens,keyval]',''],
        0x25 : ['remote','1'],
        0x26 : ['remote, config','1,38'],
        0x27 : ['remote','1'],
        0x28 : ['remote','1'],
        0x29 : ['remote, sensor','1,4'],
        0x2A : ['remote','1'],
        0x2B : ['remote','1']
        }

"""
Explicit decayChain and segment loops
"""

import BaseClasses.BSLoop as BSLoop
bslp = BSLoop.BSLoop()


print('===================')
bslp.SetVerbosity(2)
print('...Set the configuration and cut')
cV = {'configuration': 'DS5', 'cut': 1}
bslp.SetCurrentVars(**cV)
print('===================')
# For each detector, loop each hardwareComponent; and within each hardwareComponent, loop each decayChain's segments
# lowest level of recursion
recurSegment = {'r_objType': 'segment', 'r_weightFunc': 'BranchingRatio', 'r_recur': {}} # end recursion upon {}
# second lowest level of recursion
recurDecayChain = {'r_objType': 'decayChain', 'r_weightFunc': None, 'r_recur': recurSegment}
# third lowest level of recursion
recurHardwareComponent = {'r_objType': 'hardwareComponent', 'r_weightFunc': None, 'r_recur': recurDecayChain}
# top level of recursion
bslp.For(objType = 'detector', weightFunc = None, **recurHardwareComponent)

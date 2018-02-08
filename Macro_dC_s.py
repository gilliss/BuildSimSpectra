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
print('Loop over detectors; For each detector, loop over hardwareComponents; For each hardwareComponent, loop over decayChains; For each decayChain, loop over segments')
# For each detector, loop each hardwareComponent; and within each hardwareComponent, loop each decayChain's segments
# lowest level of recursion
recurSegment = {'r_objType': 'segment', 'r_weightFunc': 'BranchingRatio', 'r_recur': {}} # end recursion upon {}
# second lowest level of recursion
recurDecayChain = {'r_objType': 'decayChain', 'r_weightFunc': None, 'r_recur': recurSegment}
# third lowest level of recursion
recurHardwareComponent = {'r_objType': 'hardwareComponent', 'r_weightFunc': None, 'r_recur': recurDecayChain}
# top level of recursion
bslp.For(objType = 'detector', weightFunc = None, **recurHardwareComponent)
print('...Results are spectra: hardwareComponent_detector_decayChain_cut_configuration.*')
print('===================')
print('Loop over hardwareComponents; For each hardwareComponent, loop over decayChains; For each decayChain, loop over detectors')
recurDetector = {'r_objType': 'detector', 'r_weightFunc': 'TotalMass', 'r_recur': {}}
recurDecayChain = {'r_objType': 'decayChain', 'r_weightFunc': None, 'r_recur': recurDetector}
bslp.For(objType = 'hardwareComponent', weightFunc = None, **recurDecayChain)
print('...Results are spectra: hardwareComponent_decayChain_cut_configuration.*')
print('===================')

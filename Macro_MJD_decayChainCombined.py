"""
Mimic hierarchy of ordering used for creation of MJD_<decayChain>Combined.* hists
"""

import BaseClasses.BSLoop as BSLoop
bslp = BSLoop.BSLoop()

# BREAK THE PROCESS UP INTO STEPS SO CAN SAVE INTERMEDIATE PLOTS
print('===================')
bslp.SetVerbosity(2)
print('...Set the configuration and cut')
cV = {'configuration': 'DS5', 'cut': 1}
bslp.SetCurrentVars(**cV)
print('===================')
print('...For each detector, for each hardwareComponent, for each decayChain, add segments (add spectra: det_hw_segment)')
recurSegment = {'r_objType': 'segment', 'r_weightFunc': None, 'r_recur': {}} # end recursion upon {} # use the segment-only (no explicit decayChain loop) syntax
recurHardwareComponent = {'r_objType': 'hardwareComponent', 'r_weightFunc': None, 'r_recur': recurSegment}
bslp.For(objType = 'detector', weightFunc = 'WeightBranchingRatio', **recurHardwareComponent)
print('...Results are spectra: det_hw_chain')
print('===================')
# print('...For each detector, for each decayChain, add hardwareComponents (add spectra: det_hw_chain)')
# recurHardwareComponent = {'r_objType': 'hardwareComponent', 'r_weightFunc': None, 'r_recur': {}}
# recurDecayChain = {'r_objType': 'decayChain', 'r_weightFunc': None, 'r_recur': recurHardwareComponent}
# bslp.For(objType = 'detector', weightFunc = 'WeightAssayTimePerDetectorMass', **recurDecayChain)
# print('...Results are spectra: det_chain')
# print('===================')
# print('...For each decayChain, add detectors (add spectra: det_chain)')
# recurDetector = {'r_objType': 'detector', 'r_weightFunc': None, 'r_recur': {}}
# bslp.For(objType = 'decayChain', weightFunc = 'WeightDetectorMassPerTotalMass', **recurDetector)
# print('...Results are spectra: chain')
#print(bslp.GetCurrentVarsDict())

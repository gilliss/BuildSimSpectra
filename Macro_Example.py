"""
Macro to reproduce the sim spectra production procedure done in mjdsim/
"""

import BaseClasses.BSLoop as BSLoop
bslp = BSLoop.BSLoop()


print('===================')
print('...Set the configuration, cut, and verbosity')

configCutDict = {'configuration': 'DS5', 'cut': 1}
bslp.SetConfigCut(**configCutDict)
bslp.SetVerbosity(2)

print('===================')
print('Loop over detectors; For each detector, loop over hardwareComponents; For each hardwareComponent, loop over decayChains; For each decayChain, loop over segments')

recurSegment = {'r_objType': 'segment', 'r_weightFunc': 'BranchingRatio', 'r_recur': {}} # end recursion upon {} # lowest level of recursion
recurDecayChain = {'r_objType': 'decayChain', 'r_weightFunc': None, 'r_recur': recurSegment} # second lowest level of recursion
recurHardwareComponent = {'r_objType': 'hardwareComponent', 'r_weightFunc': None, 'r_recur': recurDecayChain} # third lowest level of recursion
bslp.For(objType = 'detector', weightFunc = None, **recurHardwareComponent) # top level of recursion

print('...Results are spectra: hardwareComponent_detector_decayChain_cut_configuration.*')
print('===================')
print('Loop over hardwareComponents; For each hardwareComponent, loop over decayChains; For each decayChain, loop over detectors')

recurDetector = {'r_objType': 'detector', 'r_weightFunc': 'TotalMass', 'r_recur': {}}
recurDecayChain = {'r_objType': 'decayChain', 'r_weightFunc': None, 'r_recur': recurDetector}
bslp.For(objType = 'hardwareComponent', weightFunc = None, **recurDecayChain)

print('...Results are spectra: hardwareComponent_decayChain_cut_configuration.*')
print('===================')
print('Loop over detectors; For each detector, loop over decayChains; For each decayChain, loop over hardwareComponents')

recurHardwareComponent = {'r_objType': 'hardwareComponent', 'r_weightFunc': 'ActivityPerDetectorMass', 'r_recur': {}}
recurDecayChain = {'r_objType': 'decayChain', 'r_weightFunc': None, 'r_recur': recurHardwareComponent}
bslp.For(objType = 'detector', weightFunc = None, **recurDecayChain)

print('...Results are spectra: detector_decayChain_cut_configuration.*')
print('===================')
print('Loop over decayChains; For each decayChain, loop over detectors')

recurDetector = {'r_objType': 'detector', 'r_weightFunc': 'DetectorMassPerTotalMass', 'r_recur': {}}
bslp.For(objType = 'decayChain', weightFunc = None, **recurDetector)

print('...Results are spectra: decayChain_cut_configuration.*')
print('===================')

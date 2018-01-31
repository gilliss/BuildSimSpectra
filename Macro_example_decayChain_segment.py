"""
As shown in the two code blocks below, can achieve equivalent results with different syntax regarding decayChain and segment looping
"""

import BaseClasses.BSLoop as BSLoop
bslp = BSLoop.BSLoop()

# For each detector, loop each hardwareComponent; and within each hardwareComponent, loop each decayChain's segments
# lowest level of recursion
recurSegment = {'r_objType': 'segment', 'r_weightFunc': None, 'r_recur': {}} # end recursion upon {}
# second lowest level of recursion
recurHardwareComponent = {'r_objType': 'hardwareComponent', 'r_weightFunc': None, 'r_recur': recurSegment}
# top level of recursion
bslp.For(objType = 'detector', weightFunc = None, **recurHardwareComponent)

# # EQUIVALENTLY: For each detector, loop each hardwareComponent; and within each hardwareComponent, loop each decayChain's segments
# # lowest level of recursion
# recurSegment = {'r_objType': 'segment', 'r_weightFunc': None, 'r_recur': {}} # end recursion upon {}
# # second lowest level of recursion
# recurDecayChain = {'r_objType': 'decayChain', 'r_weightFunc': None, 'r_recur': recurSegment}
# # third lowest level of recursion
# recurHardwareComponent = {'r_objType': 'hardwareComponent', 'r_weightFunc': None, 'r_recur': recurDecayChain}
# # top level of recursion
# bslp.For(objType = 'detector', weightFunc = None, **recurHardwareComponent)

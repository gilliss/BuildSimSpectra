"""
A test macro.
Tests import of BaseClasses/ and ConfiguratData/ modules.
Tests writing of JSON via nested loops of detector, decayChain, hardwareComponent, etc.
Tests pandas adding of spectra across rows or cols according to weightings
"""

# Test import of BaseClasses/
import BaseClasses.BSLoop as BSLoop
bslp = BSLoop.BSLoop()
print(bslp.ReturnHello())

# Test import of ConfiguratData/
import BaseClasses.BSConfigData as BSConfigData
bscfgd = BSConfigData.BSConfigData()
print(bscfgd.GetDetectorList())
print(bscfgd.GetDecayChainSegmentBranchingRatioDict())
print(bscfgd.GetDecayChainSegmentBranchingRatioDict()['U'])
for obj in bscfgd.GetDecayChainSegmentBranchingRatioDict():
    print(obj)
dcsbrd = bscfgd.GetDecayChainSegmentBranchingRatioDict()
for obj in dcsbrd['U']:
    print(obj, dcsbrd['U'][obj])

# An Example: for each segment, loop each detector
# recur = {'r_objType': 'detector', 'r_comboRule': None, 'r_recur': {}} # end recursion upon {}
# bslp.For(objType = 'segment', comboRule = None, **recur)

# An Example: for each detector, loop each decayChain; and within each decayChain, loop each segment
# recurSegment = {'r_objType': 'segment', 'r_comboRule': None, 'r_recur': {}} # end recursion upon {}
# recurDecayChain = {'r_objType': 'decayChain', 'r_comboRule': None, 'r_recur': recurSegment}
# bslp.For(objType = 'detector', comboRule = None, **recurDecayChain)

# An Example: for each segment, loop each detector
recur = {'r_objType': 'segment', 'r_comboRule': None, 'r_recur': {}} # end recursion upon {}
bslp.For(objType = 'detector', comboRule = None, **recur)

### Test BSLoop.For()
#bslp.For(objType = 'detector')
#bslp.For(objType = 'decayChain')

### Test recursive For()
#recur = {'r_objType': None, 'r_comboRule': None, 'r_recur': {}}
#recur = {'r_objType': 'detector', 'r_comboRule': None, 'r_recur': {}}
#recur = {'r_objType': 'decayChain', 'r_comboRule': None, 'r_recur': {}}
#recur = {}
# print(bslp.currentDetector, bslp.currentDecayChain)
# bslp.For(objType = 'segment', comboRule = None, **recur)
# print(bslp.currentDetector, bslp.currentDecayChain)

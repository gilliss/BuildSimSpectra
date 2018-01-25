"""
Class to find data from directory structures within mjdsim/ and elsewhere on PDSF
"""

class BSFindData():
        def __init__(self):
            self.configuration = None
            self.detector = None
            self.decayChain = None
            self.segment = None
            self.branchingRatio = None
            self.hardwareComponent = None
            self.hardwareGroup = None
            return None

        def GetFullPath(self, currentVarsDict):
            configuration, detector, decayChain, segment, branchingRatio, hardwareComponent, hardwareGroup = self.configuration, self.detector, self.decayChain, self.segment, self.branchingRatio, self.hardwareComponent, self.hardwareGroup

            configuration = currentVarsDict['configuration']
            detector = currentVarsDict['detector']
            decayChain = currentVarsDict['decayChain']
            segment = currentVarsDict['segment']
            branchingRatio = currentVarsDict['branchingRatio']
            hardwareComponent = currentVarsDict['hardwareComponent']
            hardwareGroup = currentVarsDict['hardwareGroup']

            #print(currentVarsDict)

            if configuration and detector and (not decayChain) and segment and branchingRatio and hardwareComponent and (not hardwareGroup):
                fileName = '%s_%s_%s.root' % (hardwareComponent, segment, detector)
                print('  found file', fileName)

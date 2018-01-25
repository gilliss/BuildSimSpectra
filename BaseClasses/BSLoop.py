"""
Functions to handle nested loops over different types. Loops could be nested in any order.
Types: ['detector', 'hardwareComponent', 'decayChain', 'decayChainSegment']
"""

import BaseClasses.BSConfigData as BSConfigData
bscd = BSConfigData.BSConfigData()

import BaseClasses.BSFindData as BSFindData
bsfd = BSFindData.BSFindData()

class BSLoop():
    """
    Functions to handle nested loops over different types. Loops could be nested in any order.
    Types: ['detector', 'hardwareComponent', 'decayChain', 'decayChainSegment']
    """
    def __init__(self):
        # Useful singletons for loops to know what layer they're on
        self.currentConfiguration = None
        self.currentDetector = None
        self.currentDecayChain = None
        self.currentSegment = None
        self.currentBranchingRatio = None
        self.currentHardwareComponent = None
        self.currentHardwareGroup = None
        return None

    def ResetCurrentVars(self, objType):
        self.currentConfiguration = None
        self.currentDetector = None
        self.currentDecayChain = None
        self.currentSegment = None
        self.currentBranchingRatio = None
        self.currentHardwareComponent = None
        self.currentHardwareGroup = None
        return None

    def GetCurrentVarsDict(self):
        #return [self.currentConfiguration, self.currentDetector, self.currentDecayChain, self.currentSegment, self.currentBranchingRatio, self.currentHardwareComponent, self.currentHardwareGroup]
        return {
                'configuration': self.currentConfiguration,
                'detector': self.currentDetector,
                'decayChain': self.currentDecayChain,
                'segment': self.currentSegment,
                'branchingRatio': self.currentBranchingRatio,
                'hardwareComponent': self.currentHardwareComponent,
                'hardwareGroup': self.currentHardwareGroup
                }

    def ReturnHello(self):
        return 'Hello'

    def For(self, objType = None, weightFunc = None, **recur):
        """
        Recursively call loops over objectTypes, allowing for loops to be called in arbitrary order
        objType = detector, hardwareComponent, decayChain, segment
        weightFunc = info for weighting hist in a combination
        recur = a dict of args for the next layer of recursion
        """
        if recur:
            r_objType = recur['r_objType']
            r_weightFunc = recur['r_weightFunc']
            r_recur = recur['r_recur'] #print('recur args:',r_objType, r_weightFunc, r_recur)

        if(objType == 'detector'):
            for obj in bscd.GetDetectorList():
                self.currentDetector = obj
                print('detector', self.currentDetector)
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsfd.GetFullPath(self.GetCurrentVarsDict()) # This syntax could be simplified with a BSCurrent.py class to hold the current var vals. bsfd would have access to BSCurrentVars
            self.currentDetector = None # This syntax could be simplified to BSCurrentVars.ResetVar(objType)

        if(objType == 'decayChain'):
            for obj in bscd.GetDecayChainList():
                self.currentDecayChain = obj
                print('decayChain', self.currentDecayChain) # Can comment this out if also looping over segment b/c currentDecayChain is also printed in the segment block
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsfd.GetFullPath(self.GetCurrentVarsDict())
            self.currentDecayChain = None

        if(objType == 'segment'):
            if(self.currentDecayChain == None): # This block obviates the need to separately specify looping over decayChain and segment. This block essentially does both. # This block avoids setting currentDecayChain. Must use the segment-only syntax in the macro
                for decayChain in bscd.GetDecayChainSegmentBranchingRatioDict():
                    for obj in bscd.GetDecayChainSegmentBranchingRatioDict()[decayChain]:
                        self.currentSegment = obj
                        self.currentBranchingRatio = bscd.GetDecayChainSegmentBranchingRatioDict()[decayChain][obj]
                        print('segment', decayChain, self.currentBranchingRatio)
                        if recur:
                            self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                        if not recur:
                            None#print('...end of line, finding bottom-level sim files')
                        bsfd.GetFullPath(self.GetCurrentVarsDict())
                    self.currentSegment = None
            else: # This block is called if decayChain and segment are explicity looped over separately in the macro
                for obj in bscd.GetDecayChainSegmentBranchingRatioDict()[self.currentDecayChain]:
                    self.currentSegment = obj
                    self.currentBranchingRatio = bscd.GetDecayChainSegmentBranchingRatioDict()[self.currentDecayChain][obj]
                    print('segment', self.currentDecayChain, self.currentBranchingRatio)
                    if recur:
                        self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                    if not recur:
                        None#print('...end of line, finding bottom-level sim files')
                    bsfd.GetFullPath(self.GetCurrentVarsDict())
                self.currentSegment = None
                self.currentBranchingRatio = None

        if(objType == 'hardwareComponent'):
            for obj in bscd.GetHardwareComponentList():
                self.currentHardwareComponent = obj
                print('hardwareComponent', self.currentHardwareComponent)
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsfd.GetFullPath(self.GetCurrentVarsDict())
            self.currentHardwareComponent = None

    # def TestPassDict(self, objType = None, **recur):
    #     if recur:
    #         r_objType = recur['r_objType']
    #         r_weightFunc = recur['r_weightFunc ']
    #         r_recur = recur['r_recur']
    #         print(r_objType, r_weightFunc , r_recur)

    # def For(self, objType = None, weightFunc = None, **recur):
    #     r_objType = recur['r_objType']
    #     r_weightFunc = recur['r_weightFunc ']
    #     r_recur = recur['r_recur']
    #     if(objType == 'detector'):
    #         for obj in bscd.GetDetectorList():
    #             print('detector', obj)
    #             #Recur(objType = recur_arg_dict['objType'], weightFunc = recur_arg_dict['self.current'], Recur = recur_arg_dict['Recur'])
    #     if(objType == 'hwComponent'):
    #         return objType
    #     if(objType == 'decayChain'):
    #         for obj in bscd.GetDecayChainList():
    #             print('decayChain', obj)
    #             #Recur(objType = recur_arg_dict['objType'], weightFunc = recur_arg_dict['self.current'], Recur = recur_arg_dict['Recur'])
    #     if(objType == 'segment'):
    #         return objType
    #     else:
    #         return None

if __name__ == '__main__':
    BSLoop()

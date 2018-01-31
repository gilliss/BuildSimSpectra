"""
Functions to handle nested loops over different types. Loops could be nested in any order.
Types: ['detector', 'hardwareComponent', 'decayChain', 'decayChainSegment']
"""

import BaseClasses.BSConfigData as BSConfigData
bscd = BSConfigData.BSConfigData()

import BaseClasses.BSCurrentVars as BSCurrentVars
bscv = BSCurrentVars.BSCurrentVars()

import BaseClasses.BSManageData as BSManageData
bsmd = BSManageData.BSManageData(bscv) # bsmd needs the bscv object passed into it

class BSLoop():
    """
    Functions to handle nested loops over different types. Loops could be nested in any order.
    Types: ['detector', 'hardwareComponent', 'decayChain', 'decayChainSegment', 'hardwareGroup', 'configuration', 'cut']
    """
    def __init__(self):
        print('Remember to set configuration and cut, and use desired recursion/looping routine with desired weightFuncs set')
        return None

    def ReturnHello(self):
        return 'Hello'

    def SetCurrentVars(self, **currentVars):
        bscv.SetCurrentVar('configuration', currentVars['configuration'])
        bscv.SetCurrentVar('cut', currentVars['cut'])

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
                bscv.SetCurrentVar(objType, obj)
                print(objType, bscv.GetCurrentVar(objType))
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsmd.GetFile() # This syntax could be simplified with a BSCurrent.py class to hold the current var vals. bsmd would have access to BSCurrentVars
            bscv.ResetCurrentVar(objType) # This syntax could be simplified to BSCurrentVars.ResetVar(objType)

        if(objType == 'decayChain'):
            for obj in bscd.GetDecayChainList():
                bscv.SetCurrentVar(objType, obj)
                print(objType, bscv.GetCurrentVar(objType)) # Can comment this out if also looping over segment b/c currentDecayChain is also printed in the segment block
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsmd.GetFile()
            bscv.ResetCurrentVar(objType)

        if(objType == 'segment'):
            if bscv.GetCurrentVar('decayChain') == None: # This block obviates the need to separately specify looping over decayChain and segment. This block essentially does both. # This block avoids setting currentDecayChain. Must use the segment-only syntax in the macro
                for decayChain in bscd.GetDecayChainSegmentBranchingRatioDict():
                    for obj in bscd.GetDecayChainSegmentBranchingRatioDict()[decayChain]:
                        bscv.SetCurrentVar(objType, obj)
                        bscv.SetCurrentVar('branchingRatio', bscd.GetDecayChainSegmentBranchingRatioDict()[decayChain][obj])
                        print(objType, decayChain, bscv.GetCurrentVar('branchingRatio'))
                        if recur:
                            self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                        if not recur:
                            None#print('...end of line, finding bottom-level sim files')
                        bsmd.GetFile()
                    bscv.ResetCurrentVar(objType)
            else: # This block is called if decayChain and segment are explicity looped over separately in the macro
                for obj in bscd.GetDecayChainSegmentBranchingRatioDict()[bscv.GetCurrentVar('decayChain')]:
                    bscv.SetCurrentVar(objType, obj)
                    bscv.SetCurrentVar('branchingRatio', bscd.GetDecayChainSegmentBranchingRatioDict()[bscv.GetCurrentVar('decayChain')][obj])
                    print(objType, bscv.GetCurrentVar('decayChain'), bscv.GetCurrentVar('branchingRatio'))
                    if recur:
                        self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                    if not recur:
                        None#print('...end of line, finding bottom-level sim files')
                    bsmd.GetFile()
                bscv.ResetCurrentVar(objType)
                bscv.ResetCurrentVar('branchingRatio')

        if(objType == 'hardwareComponent'):
            for obj in bscd.GetHardwareComponentList():
                bscv.SetCurrentVar(objType, obj)
                print(objType, bscv.GetCurrentVar(objType))
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsmd.GetFile()
            bscv.ResetCurrentVar(objType)

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

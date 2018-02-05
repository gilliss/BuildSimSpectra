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

import BaseClasses.BSCombine as BSCombine
bscDict = {}

class BSLoop():
    """
    Functions to handle nested loops over different types. Loops could be nested in any order.
    Types: ['detector', 'hardwareComponent', 'decayChain', 'decayChainSegment', 'hardwareGroup', 'configuration', 'cut']
    """
    def __init__(self):
        print('Remember to set configuration and cut, and use desired recursion/looping routine with desired weightFuncs set')
        return None

    def ReturnHello(self):
        print(bscd.GetDecayChainList())

    def SetVerbosity(self, setting):
        bscv.SetVerbosity(setting)

    def Print(self, *args):
        if bscv.GetCurrentVar('verbose') == 2:
            print(args)

    def SetCurrentVars(self, **currentVars):
        # make this an automatic for loop through the **currentVars dict {bascv.SetCurrentVar(obj, currentVars[obj])}
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
                self.Print(objType, bscv.GetCurrentVar(objType))
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsmd.GetData() # This syntax could be simplified with a BSCurrent.py class to hold the current var vals. bsmd would have access to BSCurrentVars
            bscv.ResetCurrentVar(objType) # This syntax could be simplified to BSCurrentVars.ResetVar(objType)

        if(objType == 'decayChain'):
            for obj in bscd.GetDecayChainList():
                bscv.SetCurrentVar(objType, obj)
                self.Print(objType, bscv.GetCurrentVar(objType)) # Can comment this out if also looping over segment b/c currentDecayChain is also printed in the segment block
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsmd.GetData()
            bscv.ResetCurrentVar(objType)

        if(objType == 'segment'):
            if bscv.GetCurrentVar('decayChain') == None: # This block obviates the need to separately specify looping over decayChain and segment. This block essentially does both. # This block avoids setting currentDecayChain. Must use the segment-only syntax in the macro
                for decayChain in bscd.GetDecayChainSegmentBranchingRatioDict():
                    bscDict[objType] = BSCombine.BSCombine(weightFunc) # BSCombineData instantiate for each decayChain
                    for obj in bscd.GetDecayChainSegmentBranchingRatioDict()[decayChain]:
                        bscv.SetCurrentVar(objType, obj)
                        bscv.SetCurrentVar('branchingRatio', bscd.GetDecayChainSegmentBranchingRatioDict()[decayChain][obj])
                        self.Print(objType, decayChain, bscv.GetCurrentVar('branchingRatio'))
                        data = []
                        if recur:
                            data = self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                        if not recur:
                            data = bsmd.GetData() # bscDict[objType].Add(bsmd.GetData())
                        bscDict[objType].Add(data) # add data into combo for this level
                    bscv.ResetCurrentVar(objType)
                    bsmd.Save(bscDict[objType].GetCombinedData()) # save the combo of this level
                    del bscDict[objType] # del BSCombineData instance
            else: # This block is called if decayChain and segment are explicity looped over separately in the macro
                for obj in bscd.GetDecayChainSegmentBranchingRatioDict()[bscv.GetCurrentVar('decayChain')]:
                    bscv.SetCurrentVar(objType, obj)
                    bscv.SetCurrentVar('branchingRatio', bscd.GetDecayChainSegmentBranchingRatioDict()[bscv.GetCurrentVar('decayChain')][obj])
                    self.Print(objType, bscv.GetCurrentVar('decayChain'), bscv.GetCurrentVar('branchingRatio'))
                    if recur:
                        self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                    bsmd.GetData()
                bscv.ResetCurrentVar(objType)
                bscv.ResetCurrentVar('branchingRatio')

        if(objType == 'hardwareComponent'):
            for obj in bscd.GetHardwareComponentList():
                bscv.SetCurrentVar(objType, obj)
                self.Print(objType, bscv.GetCurrentVar(objType))
                if recur:
                    self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
                bsmd.GetData()
            bscv.ResetCurrentVar(objType)

        return combinedData

if __name__ == '__main__':
    BSLoop()

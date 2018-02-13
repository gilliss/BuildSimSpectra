"""
Functions to handle nested loops over different types. Loops could be nested in any order.
Types: ['detector', 'hardwareComponent', 'decayChain', 'decayChainSegment']
"""

import BaseClasses.BSCurrentVars as BSCurrentVars
bscv = BSCurrentVars.BSCurrentVars()

import BaseClasses.BSConfigData as BSConfigData
bscd = BSConfigData.BSConfigData(bscv)

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
        # this function should probably inherit from/be implemented in BSCurrentVars
        bscv.SetCurrentVar('configuration', currentVars['configuration'])
        bscv.SetCurrentVar('cut', currentVars['cut'])

    def GetBSCDList(self, objType):
        """
        Return the list or dict of objs of this objType. To be looped over in the For() routine.
        """
        if(objType == 'detector'):
            return bscd.GetActiveDetectorSNList()
        if(objType == 'decayChain'):
            return bscd.GetDecayChainList()
        if(objType == 'segment'):
            return bscd.GetDecayChainSegmentBranchingRatioDict()[bscv.GetCurrentVar('decayChain')]
        if(objType == 'hardwareComponent'):
            return bscd.GetHardwareComponentList()

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

        bscDict[objType] = BSCombine.BSCombine(weightFunc, bscv, bscd) # BSCombine instantiation for each loop
        for obj in self.GetBSCDList(objType):
            bscv.SetCurrentVar(objType, obj)
            if objType == 'segment': # could remove this special case if branchingRatio was treated as its own loop
                bscv.SetCurrentVar('branchingRatio', self.GetBSCDList(objType)[obj])
            self.Print(objType, bscv.GetCurrentVar(objType))
            if recur:
                data = self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
            if not recur:
                data = bsmd.GetData() # return the data from lower level of recursion up into this loop
            if (data is not None):
                bsmd.Save(data, sDat = True, sFig = True) # save the data that got fed in
                if (weightFunc != None):
                    bscDict[objType].Add(data) # add data into combo for this level
        bscv.ResetCurrentVar(objType)
        if objType == 'segment': # could remove this special case if branchingRatio was treated as its own loop
            bscv.ResetCurrentVar('branchingRatio')
        if weightFunc != None and (data is not None):
            return bscDict[objType].GetCombinedData()

        return None # return None if not doing any combining at this level (i.e. no data or weightFunc)

        # if(objType == 'detector'):
        #     # MAKE activeDetectorSNList # I should make this an object in the ConfigData file ...
        #     activeDetectorSNList = bscd.GetActiveDetectorSNList()
        #     # LOOP OVER DETECTORS
        #     bscDict[objType] = BSCombine.BSCombine(weightFunc, bscv, bscd) # BSCombine instantiation for each loop
        #     for obj in activeDetectorSNList: #bscd.GetDetectorList():
        #         bscv.SetCurrentVar(objType, obj)
        #         self.Print(objType, bscv.GetCurrentVar(objType)) # Can comment this out if also looping over segment b/c currentDecayChain is also printed in the segment block
        #         if recur:
        #             data = self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
        #         if not recur:
        #             data = bsmd.GetData() # return the data up into these loops
        #         if (data is not None):
        #             bsmd.Save(data, sDat = True, sFig = True) # save the data that got fed in
        #             if (weightFunc != None):
        #                 bscDict[objType].Add(data) # add data into combo for this level
        #     bscv.ResetCurrentVar(objType)
        #     if weightFunc != None and (data is not None):
        #         return bscDict[objType].GetCombinedData()

        # if(objType == 'decayChain'):
        #     bscDict[objType] = BSCombine.BSCombine(weightFunc, bscv, bscd) # BSCombine instantiation for each loop
        #     for obj in bscd.GetDecayChainList():
        #         bscv.SetCurrentVar(objType, obj)
        #         self.Print(objType, bscv.GetCurrentVar(objType)) # Can comment this out if also looping over segment b/c currentDecayChain is also printed in the segment block
        #         if recur:
        #             data = self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
        #         if not recur:
        #             data = bsmd.GetData() # return the data up into these loops
        #         if (data is not None):
        #             bsmd.Save(data, sDat = True, sFig = True) # save the data that got fed in
        #             if (weightFunc != None):
        #                 bscDict[objType].Add(data) # add data into combo for this level
        #     bscv.ResetCurrentVar(objType)
        #     if weightFunc != None and (data is not None):
        #         return bscDict[objType].GetCombinedData()

        # if(objType == 'segment'):
        #         bscDict[objType] = BSCombine.BSCombine(weightFunc, bscv, bscd) # BSCombine instantiation for each loop
        #         for obj in bscd.GetDecayChainSegmentBranchingRatioDict()[bscv.GetCurrentVar('decayChain')]:
        #             bscv.SetCurrentVar(objType, obj)
        #             bscv.SetCurrentVar('branchingRatio', bscd.GetDecayChainSegmentBranchingRatioDict()[bscv.GetCurrentVar('decayChain')][obj])
        #             self.Print(objType, bscv.GetCurrentVar('decayChain'), bscv.GetCurrentVar('segment'), bscv.GetCurrentVar('branchingRatio'))
        #             if recur:
        #                 data = self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
        #             if not recur:
        #                 data = bsmd.GetData() # return the data up into these loops
        #             if (data is not None):
        #                 bsmd.Save(data, sDat = True, sFig = True) # save the data that got fed in
        #                 if (weightFunc != None):
        #                     bscDict[objType].Add(data) # add data into combo for this level
        #         bscv.ResetCurrentVar(objType)
        #         bscv.ResetCurrentVar('branchingRatio')
        #         if weightFunc != None and (data is not None): # note that this block comes AFTER reseting current vars. This is so that the current vars represent the COMBO hist
        #             return bscDict[objType].GetCombinedData()

        # if(objType == 'hardwareComponent'):
        #     bscDict[objType] = BSCombine.BSCombine(weightFunc, bscv, bscd) # BSCombine instantiation for each loop
        #     for obj in bscd.GetHardwareComponentList():
        #         bscv.SetCurrentVar(objType, obj)
        #         self.Print(objType, bscv.GetCurrentVar(objType))
        #         if recur:
        #             data = self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur)
        #         if not recur:
        #             data = bsmd.GetData() # return the data up into these loops
        #         if (data is not None):
        #             bsmd.Save(data, sDat = True, sFig = True) # save the data that got fed in
        #             if (weightFunc != None):
        #                 bscDict[objType].Add(data) # add data into combo for this level
        #     bscv.ResetCurrentVar(objType)
        #     if weightFunc != None and (data is not None):
        #         return bscDict[objType].GetCombinedData()


if __name__ == '__main__':
    BSLoop()

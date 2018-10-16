"""
Functions to handle nested loops over different types. Loops could be nested in any order.
Types: ['detector', 'hardwareComponent', 'decayChain', 'decayChainSegment']
In macro that calls this class, remember to set verbosity, configuration and cut, saveData and saveFigure, and use desired recursion/looping routine with desired weightFuncs set.
"""

import BaseClasses.BSCurrentVars as BSCurrentVars
bscv = BSCurrentVars.BSCurrentVars()

import BaseClasses.BSConfigData as BSConfigData
bscd = BSConfigData.BSConfigData(bscv) # note bscv object is passed in

import BaseClasses.BSManageData as BSManageData
bsmd = BSManageData.BSManageData(bscd) # note bscd object (which holds a bscv object) is passed in

import BaseClasses.BSCombine as BSCombine
bscDict = {} # BSCombine instances are instantiated and added into this dict in the For() method

class BSLoop():
    """
    Functions to handle nested loops over different types. Loops could be nested in any order.
    Types: ['detector', 'hardwareComponent', 'decayChain', 'segment', 'hardwareGroup', 'configuration', 'cut']
    """
    def __init__(self):
        self.saveData = False
        self.saveFigure = False
        return None

    def Print(self, val, *args):
        if val <= bscv.GetCurrentVar('verbosity'): # 0 = Error, 1 = Some, 2 = More, 3 = Debug
            print(args)

    def SetVerbosity(self, setting):
        bscv.SetVerbosity(setting)

    def SetSave(self, sDat = False, sFig = False):
        self.saveData = sDat
        self.saveFigure = sFig

    def SetMacroData(self, objType, inData = None):
        bscd.SetMacroData(objType = objType, inData = inData)

    def SetConfigCut(self, **currentVars):
        bscv.SetCurrentVar('configuration', currentVars['configuration'])
        bscv.SetCurrentVar('cut', currentVars['cut'])

    def GetBSCDList(self, objType):
        """
        Return the list or dict of objs of this objType directly from BSConfigData
        """
        if(objType == 'activeDetectorSNList'):
            return bscd.GetActiveDetectorSNList()
        if(objType == 'activeEnrichedDetectorSNList'):
            return bscd.GetActiveEnrichedDetectorSNList()
        if(objType == 'hardwareComponentList'):
            return bscd.GetHardwareComponentList()
        if(objType == 'decayChainList'):
            return bscd.GetDecayChainList()

    def GetMacroList(self, objType):
        """
        Return the list or dict of objs of this objType. To be looped over in the For() routine.
        """
        if(objType == 'segment'):
            # Special case for segment b/c this GetMacroData('segment') call returns a dict, rather than a list
            return bscd.GetMacroData(objType)[bscv.GetCurrentVar('decayChain')] #return bscd.GetDecayChainSegmentBranchingRatioDict()[bscv.GetCurrentVar('decayChain')]
        else:
            return bscd.GetMacroData(objType)

    def For(self, objType = None, weightFunc = None, **recur):
        """
        Recursively call loops over objectTypes, allowing for loops to be called in arbitrary order
        objType = detector, hardwareComponent, decayChain, segment
        weightFunc = info for weighting hist in a combination
        recur = a dict of args for the next layer of recursion

        Notes on current implementation:
        -You only pull .npy or .root data if you don’t recur (that is, if you’re at the top of the LIFO recursion stack). Otherwise, data gets returned up into your loop.
        -You only save if you pull non-null data (not desired: current implementation resaves .npy data that get pulled)
        -Combined data is returned to the next loop up if weightFunc is set, even if combinedData is zeros
        -You only combine data if the pulled data is not None and the weightFunc is set
        -By pull, I mean bsmd.GetData()
        -If data is None (i.e. DNE), then the loop just passes by without doing any operations
        """
        if recur:
            r_objType = recur['r_objType']
            r_weightFunc = recur['r_weightFunc']
            r_recur = recur['r_recur']
            self.Print(3, 'Debug', 'recur args:', r_objType, r_weightFunc, r_recur)

        # THIS IS THE MAIN RECURSIVE LOOP. IT LOOPS, PULLS DATA, SAVES DATA, COMBINES DATA, RETURNS DATA
        bscDict[objType] = BSCombine.BSCombine(weightFunc, bscv, bscd) # BSCombine instantiation for each loop
        for obj in self.GetMacroList(objType): # loop over the objs of this objType
            bscv.SetCurrentVar(objType, obj) # set the current var for this objType. Informs the paths to files, the data pulled for weighting functions, etc.
            if objType == 'segment': # could remove this special case if branchingRatio was treated as its own loop
                bscv.SetCurrentVar('branchingRatio', self.GetMacroList(objType)[obj])
            self.Print(1, objType, bscv.GetCurrentVar(objType))
            if recur:
                data = self.For(objType = r_objType, weightFunc = r_weightFunc , **r_recur) # enter deeper level of recursion and return the results back up into this loop
            if not recur:
                data = bsmd.GetData() # return the data from lower level of recursion up into this loop
            if (data is not None):
                bsmd.Save(data, sDat = self.saveData, sFig = self.saveFigure) # save the data that got fed in
                if (weightFunc != None):
                    bscDict[objType].Add(data) # add data into combo for this level
        bscv.ResetCurrentVar(objType) # erase the current var for this objType since we are exiting the level of recursion owned by this objType.
        if objType == 'segment': # could remove this special case if branchingRatio was treated as its own loop
            bscv.ResetCurrentVar('branchingRatio')
        if weightFunc != None: #and (data is not None):
            return bscDict[objType].GetCombinedData() # return the weight-combined histogram

        return None # return None if not doing any combining at this level (i.e. no data or weightFunc)

if __name__ == '__main__':
    BSLoop()

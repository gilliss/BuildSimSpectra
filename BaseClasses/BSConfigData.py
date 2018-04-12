"""
Functions to pull out the info in ConfigurationData/
"""

import BaseClasses.ConfigurationData.Private_ConfigData as ConfigData # Insert your desired config data as BaseClasses.ConfigurationData.<>
cfgd = ConfigData.ConfigData()

class BSConfigData():
    def __init__(self, BSCurrentVarsObject):
        self.bscv = BSCurrentVarsObject # bscv object is fed in as a data member. Fed from BSLoop.py
        self.cut = None
        self.configuration = None
        self.detector = None
        self.decayChain = None
        self.segment = None
        self.branchingRatio = None
        self.hardwareComponent = None
        self.hardwareGroup = None

        self.macroDetectorSNList = None
        self.macroDecayChainList = None
        self.macroDecayChainSegmentBranchingRatioDict = None
        self.macroHardwareComponentList = None
        return None

    def UpdateSelfCurrentVars(self):
        cvDict = self.bscv.GetCurrentVarsDict()
        self.cut = cvDict['cut']
        self.configuration = cvDict['configuration']
        self.detector = cvDict['detector']
        self.decayChain = cvDict['decayChain']
        self.segment = cvDict['segment']
        self.branchingRatio = cvDict['branchingRatio']
        self.hardwareComponent = cvDict['hardwareComponent']
        self.hardwareGroup = cvDict['hardwareGroup']

    ###############################
    ###############################
    ### MacroData Methods
    ###############################
    ###############################

    def SetMacroData(self, objType = None, inData = None):
        """
        Set the custom list of objects that will be looped over by the macro.
        Useful for custom specification of inputs to a spectrum, and for splitting up spectrum building into multiple jobs
        """
        if inData == 'default':
            if(objType == 'detector'):
                self.macroDetectorSNList = self.GetActiveDetectorSNList()
            if(objType == 'decayChain'):
                self.macroDecayChainList = self.GetDecayChainList()
            if(objType == 'segment'):
                self.macroDecayChainSegmentBranchingRatioDict = self.GetDecayChainSegmentBranchingRatioDict()
            if(objType == 'hardwareComponent'):
                self.macroHardwareComponentList = self.GetHardwareComponentList()
        else:
            if(objType == 'detector'):
                self.macroDetectorSNList = inData
            if(objType == 'decayChain'):
                self.macroDecayChainList = inData
            if(objType == 'segment'):
                self.macroDecayChainSegmentBranchingRatioDict = inData
            if(objType == 'hardwareComponent'):
                self.macroHardwareComponentList = inData

    def GetMacroData(self, objType):
        """
        Get the custom list of objects that will be looped over by the macro.
        """
        if(objType == 'detector'):
            return self.macroDetectorSNList
        if(objType == 'decayChain'):
            return self.macroDecayChainList
        if(objType == 'segment'):
            return self.macroDecayChainSegmentBranchingRatioDict
        if(objType == 'hardwareComponent'):
            return self.macroHardwareComponentList

    ###############################
    ###############################
    ### Access Full ConfigData Methods
    ###############################
    ###############################

    ###############################
    ### Detectors
    ###############################
    def GetConfigurationList(self):
        return cfgd.configurationList
    def GetActiveDetectorDict(self):
        return cfgd.activeDetectorDict
    def GetDetectorList(self):
        """
        Get list of all detector simulation names (Ge_C_P_D)
        """
        return cfgd.detectorList
    def GetDetectorMassList(self):
        return cfgd.detectorMassList
    def GetEnrichedDetectorList(self):
        return cfgd.enrichedDetectorList

    def GetActiveDetectorSNList(self):
        """
        Use the current configuration's full activeDetectorDict to make a list of only the active detector serial numbers (SNs).
        The returned activeDetectorSNList does not need to correspond 1-to-1 with the (potentially custom) macroDetectorSNList.
        This is because only the macroDetectorSNList will be looped over in BSLoop.py and the SNs/masses of those detectors will be found in the activeDetectorSNList in BSCombine.py::GetWeight().
        """
        self.UpdateSelfCurrentVars()
        activeDetectorSNList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1:
                activeDetectorSNList.append(self.GetDetectorList()[i])
        return activeDetectorSNList
    def GetActiveDetectorMassList(self):
        """
        Use the current configuration's activeDetectorDict to make a list of only the active detectors' masses.
        The returned activeDetectorMassList does not need to correspond 1-to-1 with the (potentially custom) macroDetectorSNList.
        This is because only the macroDetectorSNList will be looped over in BSLoop.py and the SNs/masses of those detectors will be found in the activeDetectorSNList in BSCombine.py::GetWeight().
        """
        self.UpdateSelfCurrentVars()
        activeDetectorMassList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1:
                activeDetectorMassList.append(self.GetDetectorMassList()[i])
        return activeDetectorMassList

    ###############################
    ### Decay Chains, Segments, Branching Ratios
    ###############################
    def GetDecayChainList(self):
        return cfgd.decayChainList
    def GetDecayChainSegmentBranchingRatioDict(self):
        """
        Returns a two-level dict mapping from decayChains to their segments, and then from segments to their branchingRatio.
        """
        return cfgd.decayChainSegmentBranchingRatioDict

    ###############################
    ### Hardware Components and Assay
    ###############################
    def GetSecsPerYear(self):
        """
        Constant converting from seconds to years
        """
        return cfgd.secs_per_year
    def GetHardwareComponentDict(self):
        """
        Get the dict of hardwareComponents and their corresponding materials, masses, activations, activities
        """
        return cfgd.hardwareComponentDict
    def GetHardwareComponentList(self):
        """
        Simple list of hardwareComponents to loop over
        """
        hardwareComponentList = []
        for obj in self.GetHardwareComponentDict():
            hardwareComponentList.append(obj)
        return hardwareComponentList

if __name__ == '__main__':
    BSConfigData()

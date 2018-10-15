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
        Get list of all detector simulation names (Ge_C_P_D), regardless of config
        """
        return cfgd.detectorList
    def GetDetectorMassList(self):
        """
        Get list of all modeled masses, regardless of config
        """
        return cfgd.detectorMassList
    def GetDetectorPhysMassList(self):
        """
        Get list of all physical/measured masses, regardless of config
        """
        return cfgd.detectorPhysMassList
    def GetEnrichedDetectorList(self):
        """
        Get list of all detectors' enrichment types (0::Nat,1::Enr), regardless of config
        """
        return cfgd.enrichedDetectorList
    def GetEnrichedDetectorSNList(self):
        """
        Get list of all enr detector simulation names (Ge_C_P_D), regardless of config
        """
        self.UpdateSelfCurrentVars()
        enrichedDetectorSNList = []
        for i in range(len(self.GetDetectorList())):
            if self.GetEnrichedDetectorList()[i] == 1:
                enrichedDetectorSNList.append(self.GetDetectorList()[i])
        return enrichedDetectorSNList
    def GetNaturalDetectorSNList(self):
        """
        Get list of all nat detector simulation names (Ge_C_P_D), regardless of config
        """
        self.UpdateSelfCurrentVars()
        naturalDetectorSNList = []
        for i in range(len(self.GetDetectorList())):
            if self.GetEnrichedDetectorList()[i] == 0:
                naturalDetectorSNList.append(self.GetDetectorList()[i])
        return naturalDetectorSNList

    def GetActiveDetectorSNList(self):
        """
        Use the current configuration's activeDetectorDict to make a list of only the active detector serial numbers (SNs).
        The returned activeDetectorSNList does not need to correspond 1-to-1 with the (potentially custom) macroDetectorSNList.
        This is because only the macroDetectorSNList will be looped over in BSLoop.py and the SNs/masses of those
        detectors will be found in the activeDetectorSNList in BSCombine.py::GetWeight().
        """
        self.UpdateSelfCurrentVars()
        activeDetectorSNList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1:
                activeDetectorSNList.append(self.GetDetectorList()[i])
        return activeDetectorSNList
    def GetActiveEnrichedDetectorSNList(self):
        """
        Use the current configuration's activeDetectorDict and cfgd.enrichedDetectorList to construct a list of
        active enriched detectors
        """
        self.UpdateSelfCurrentVars()
        activeEnrichedDetectorSNList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1 and cfgd.enrichedDetectorList[i] == 1:
                activeEnrichedDetectorSNList.append(cfgd.detectorList[i])
        return activeEnrichedDetectorSNList
    def GetActiveNaturalDetectorSNList(self):
        """
        Use the current configuration's activeDetectorDict and cfgd.enrichedDetectorList to construct a list of
        active natural detectors
        """
        self.UpdateSelfCurrentVars()
        activeNaturalDetectorSNList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1 and cfgd.enrichedDetectorList[i] == 0:
                activeNaturalDetectorSNList.append(cfgd.detectorList[i])
        return activeNaturalDetectorSNList
    def GetActiveDetectorMassList(self):
        """
        Use the current configuration's activeDetectorDict to make a list of only the active detectors' masses.
        The returned activeDetectorMassList does not need to correspond 1-to-1 with the (potentially custom) macroDetectorSNList.
        This is because only the macroDetectorSNList will be looped over in BSLoop.py and the SNs/masses of those
        detectors will be found in the activeDetectorSNList in BSCombine.py::GetWeight().
        """
        self.UpdateSelfCurrentVars()
        activeDetectorMassList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1:
                activeDetectorMassList.append(self.GetDetectorMassList()[i]) # GetDetectorPhysMassList
        return activeDetectorMassList
    def GetActiveEnrichedDetectorMassList(self):
        """
        Use the current configuration's activeDetectorDict and cfgd.enrichedDetectorList to make a list
        of only the active enriched detectors' masses.
        """
        self.UpdateSelfCurrentVars()
        activeEnrichedDetectorMassList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1 and cfgd.enrichedDetectorList[i] == 1:
                activeEnrichedDetectorMassList.append(self.GetDetectorMassList()[i]) # GetDetectorPhysMassList
        return activeEnrichedDetectorMassList
    def GetActiveNaturalDetectorMassList(self):
        """
        Use the current configuration's activeDetectorDict and cfgd.enrichedDetectorList to make a list
        of only the active natural detectors' masses.
        """
        self.UpdateSelfCurrentVars()
        activeNaturalDetectorMassList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1 and cfgd.enrichedDetectorList[i] == 0:
                activeNaturalDetectorMassList.append(self.GetDetectorMassList()[i]) # GetDetectorPhysMassList
        return activeNaturalDetectorMassList

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
    def GetSegmentList(self):
        segmentList = []
        for dC in self.GetDecayChainList():
            for segment in self.GetDecayChainSegmentBranchingRatioDict()[dC]:
                segmentList.append(segment)
        segmentList = list(set(segmentList)) # remove duplicates, e.g. A222_Z86
        return segmentList

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
    def GetAssayDict(self):
        """
        Get the dict of hardwareGroups and their corresponding assay values
        """
        return cfgd.assayDict
    def GetHardwareComponentList(self):
        """
        Simple list of hardwareComponents to loop over
        """
        hardwareComponentList = []
        for obj in self.GetHardwareComponentDict():
            hardwareComponentList.append(obj)
        return hardwareComponentList
    def GetHardwareGroupList(self):
        """
        Simple list of hardwareGroups to loop over
        """
        hardwareGroupList = []
        for obj in self.GetAssayDict():
            hardwareGroupList.append(obj)
        return hardwareGroupList

if __name__ == '__main__':
    BSConfigData()

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
    ### Detectors
    ###############################
    ###############################
    def GetConfigurationList(self):
        return cfgd.configurationList
    def GetActiveDetectorDict(self):
        return cfgd.activeDetectorDict
    def GetDetectorList(self):
        return cfgd.detectorList
    def GetDetectorMassList(self):
        return cfgd.detectorMassList
    def GetEnrichedDetectorList(self):
        return cfgd.enrichedDetectorList

    def GetActiveDetectorSNList(self):
        """
        Use the current configuration's activeDetectorDict to make a list of only the active detector serial numbers (SNs)
        Note: The way this is coded now, any custom configuration of detectors (returned by GetActiveDetectorDict) has to line up with the indices of GetDetectorList.
        To satisfy this, just put zeros in the activeDetectorDict wherever you don't want a detector.
        """
        self.UpdateSelfCurrentVars()
        activeDetectorSNList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1:
                activeDetectorSNList.append(self.GetDetectorList()[i])
        return activeDetectorSNList
    def GetActiveDetectorMassList(self):
        """
        Use the current configuration's activeDetectorDict to make a list of only the active detectors' masses
        """
        self.UpdateSelfCurrentVars()
        activeDetectorMassList = []
        for i in range(len(self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
            if self.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1:
                activeDetectorMassList.append(self.GetDetectorMassList()[i])
        return activeDetectorMassList

    ###############################
    ###############################
    ### Decay Chains, Segments, Branching Ratios
    ###############################
    ###############################
    def GetDecayChainList(self):
        return cfgd.decayChainList
    def GetDecayChainSegmentBranchingRatioDict(self):
        return cfgd.decayChainSegmentBranchingRatioDict

    ###############################
    ###############################
    ### Hardware Components and Assay
    ###############################
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

"""
Functions to pull out the info in ConfigurationData/
"""

import BaseClasses.ConfigurationData.Private_ConfigData as ConfigData # Insert your desired config data as BaseClasses.ConfigurationData.<>
cfgd = ConfigData.ConfigData()

class BSConfigData():
    def __init__(self):
        return None

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
    def GetDecayChainList(self):
        return cfgd.decayChainList
    def GetDecayChainSegmentBranchingRatioDict(self):
        return cfgd.decayChainSegmentBranchingRatioDict
    def GetHardwareComponentList(self):
        return cfgd.hardwareComponentList

if __name__ == '__main__':
    BSConfigData()

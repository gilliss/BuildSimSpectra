"""
Functions to pull out the info in ConfigurationData/
"""

import BaseClasses.ConfigurationData.ConfigData as ConfigData
cfgd = ConfigData.ConfigData()

class BSConfigData():
    def __init__(self):
        return None

    def GetDetectorList(self):
        return cfgd.detectorList
    def GetDecayChainList(self):
        return cfgd.decayChainList
    def GetDecayChainSegmentBranchingRatioDict(self):
        return cfgd.decayChainSegmentBranchingRatioDict
    def GetHardwareComponentList(self):
        return cfgd.hardwareComponentList

if __name__ == '__main__':
    BSConfigData()

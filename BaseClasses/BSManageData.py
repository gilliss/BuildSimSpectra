"""
Class to find data from directory structures within mjdsim/ and elsewhere on PDSF
"""

import os

# import BaseClasses.BSCurrentVars as BSCurrentVars # A bscv object is fed in as a data member
# bscv = BSCurrentVars.BSCurrentVars()

import BaseClasses.BSPyROOT as BSPyROOT
bspr = BSPyROOT.BSPyROOT()

class BSManageData():
        """
        Class to find data from directory structures within mjdsim/ and elsewhere on PDSF
        Methods to retrieve that data and return it as a useable object to be saved or combined.
        """
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

            self.basePathMJDSIM = '/global/projecta/projectdirs/majorana/sim/MJDG41003GAT/Spectra/'
            return None

        def Print(self, *args):
            if self.bscv.GetCurrentVar('verbose') > 0:
                print(args)

        def GetFullPath(self):
            """
            Get the full path to a file. Many variants based on what weightFuncs are on or off or what level of loop you in
            """
            configuration, detector, decayChain, segment, branchingRatio, hardwareComponent, hardwareGroup = self.configuration, self.detector, self.decayChain, self.segment, self.branchingRatio, self.hardwareComponent, self.hardwareGroup

            cvDict = self.bscv.GetCurrentVarsDict()
            cut = cvDict['cut']
            configuration = cvDict['configuration']
            detector = cvDict['detector']
            decayChain = cvDict['decayChain']
            segment = cvDict['segment']
            branchingRatio = cvDict['branchingRatio']
            hardwareComponent = cvDict['hardwareComponent']
            hardwareGroup = cvDict['hardwareGroup']

            #print(cvDict)
            # FILES LIKE: DUCopper_A210_Z81_1010102.root
            if cut and configuration and detector and (not decayChain) and segment and branchingRatio and hardwareComponent and (not hardwareGroup):
                pathToFile = self.basePathMJDSIM + configuration + '/bulk/' + hardwareComponent + '/' + segment + '/'
                fileName = '%s_%s_%s.root' % (hardwareComponent, segment, detector)
                fullPathToFile = pathToFile + fileName
                if(os.path.isfile(fullPathToFile)):
                    #self.Print('  found file', fileName)
                    return fullPathToFile
                else:
                    #self.Print('  did NOT find file', fileName)
                    return None

        def GetFile(self):
            """
            Get the file and return an object that is useable
            """
            fullPathToFile = self.GetFullPath()
            #self.Print(fullPathToFile)
            return fullPathToFile # return BSPyROOT.GetHist(fullPath)

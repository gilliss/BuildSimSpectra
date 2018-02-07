"""
Class to find data from directory structures within mjdsim/ and elsewhere on PDSF
"""

import os

# import BaseClasses.BSCurrentVars as BSCurrentVars # A bscv object is fed in as a data member
# bscv = BSCurrentVars.BSCurrentVars()

import BaseClasses.BSPyROOT as BSPyROOT
bspr = BSPyROOT.BSPyROOT()

import numpy as np
import matplotlib.pyplot as plt

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
            self.basePathWrite = '/global/homes/g/gilliss/BuildSpectra_Output/'

            return None

        def Print(self, *args):
            if self.bscv.GetCurrentVar('verbose') > 0:
                print(args)

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

        def Save(self, data, sDat, sFig):
            print('  Hist integral (np.sum) =', np.sum(data))

            xArray = np.arange(bspr.xmin + 0.5, bspr.xmax + 0.5) # to be used as list of bin edges (np treats last number as INCLUDED upper edge of last been)

            plt.step(xArray, data, where = 'mid', color='k')
            if np.sum(data) > 0:
                plt.yscale('log')#, nonposy='clip')
            plt.xlim(bspr.xmin, bspr.xmax)

            if self.GetWritePath() != None:
                if sDat == True:
                    fileName = self.GetWritePath() # numpy will automatically append .npy
                    self.Print('  Saving data', fileName + '.npy')
                    np.save(fileName, data, allow_pickle = False)
                if sFig == True:
                    fileName = self.GetWritePath() + '.pdf'
                    self.Print('  Saving figure', fileName)
                    plt.savefig(fileName)
            else:
                self.Print('  SaveFig: GetWritePath is None. Not saving.')

        def GetReadPath(self):
            """
            Get the full path to a file. Many variants based on what weightFuncs are on or off or what level of loop you're in
            """
            self.UpdateSelfCurrentVars()

            fullPathToFile = ''

            # FILES LIKE: DUCopper_A210_Z81_1010102.root
            if self.cut and self.configuration and self.detector and self.decayChain and self.segment and self.branchingRatio and self.hardwareComponent and (not self.hardwareGroup):
                pathToFile = self.basePathMJDSIM + self.configuration + '/bulk/' + self.hardwareComponent + '/' + self.segment + '/'
                fileName = '%s_%s_%s.root' % (self.hardwareComponent, self.segment, self.detector)
                fullPathToFile = pathToFile + fileName

            # RETURN
            if(os.path.isfile(fullPathToFile)):
                return fullPathToFile
            else:
                self.Print('  GetReadPath: No case matching this data.')
                return None

        def GetWritePath(self):
            """
            Get the full path for where to put a file. Many variants based on what weightFuncs are on or off or what level of loop you're in
            """
            self.UpdateSelfCurrentVars()

            fullPathToFile = ''

            if self.cut and self.configuration and self.detector and self.decayChain and self.segment and self.branchingRatio and self.hardwareComponent and (not self.hardwareGroup):
                pathToFile = self.basePathWrite
                fileName = '%s_%s_%s' % (self.hardwareComponent, self.segment, self.detector)
                fullPathToFile = pathToFile + fileName

            if self.cut and self.configuration and self.detector and self.decayChain and (not self.segment) and (not self.branchingRatio) and self.hardwareComponent and (not self.hardwareGroup):
                pathToFile = self.basePathWrite
                fileName = '%s_%s_%sCombined_%s' % (self.hardwareComponent, self.detector, self.decayChain, str(self.cut))
                fullPathToFile = pathToFile + fileName

            # RETURN
            if fullPathToFile != None:
                return fullPathToFile
            else:
                self.Print('  GetWritePath: No case matching this data.')
                return None

        def GetData(self):
            """
            Get the file and return an object that is useable
            """

            fullPathToFile = self.GetReadPath()
            if fullPathToFile != None:
                cvDict = self.bscv.GetCurrentVarsDict()
                if self.basePathMJDSIM in fullPathToFile:
                    return bspr.GetBinnedData(inFile = fullPathToFile, **cvDict)
            else:
                return []

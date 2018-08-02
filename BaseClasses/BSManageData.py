"""
Class to find data from directory structures within mjdsim/ and elsewhere on PDSF
"""

import os

import BaseClasses.BSPyROOT as BSPyROOT # bspr object is instantiated as a data member upon __init__

import numpy as np
import matplotlib.pyplot as plt

class BSManageData():
        """
        Class to find data from directory structures within mjdsim/ and elsewhere on PDSF
        Methods to retrieve that data and return it as a useable object to be saved or combined.
        """
        def __init__(self, BSCurrentVarsObject):
            self.bscv = BSCurrentVarsObject # bscv object is fed in as a data member. Fed from BSLoop.py
            self.bspr = BSPyROOT.BSPyROOT(self.bscv) # note bscv object is passed in
            self.cut = None
            self.configuration = None
            self.detector = None
            self.decayChain = None
            self.segment = None
            self.branchingRatio = None
            self.hardwareComponent = None
            self.hardwareGroup = None

            self.basePathMJDSIM = '/global/projecta/projectdirs/majorana/sim/MJDG41004GAT/Spectra'
            self.basePathOutput = '/global/homes/g/gilliss/BuildSpectra_Output'

            return None

        def Print(self, val, *args):
            if val <= self.bscv.GetCurrentVar('verbosity'): # 0 = Error, 1 = Some, 2 = More, 3 = Debug
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

            self.verbosity = cvDict['verbosity']

        def GetReadPath(self):
            """
            Get the full path to a file. Many variants based on what weightFuncs are on or off or what level of loop you're in
            """
            self.UpdateSelfCurrentVars()

            fullPathToFile = ''

            self.Print(3, 'Debug', '  cVs:', self.cut, self.configuration, self.detector, self.decayChain, self.segment, self.branchingRatio, self.hardwareComponent, self.hardwareGroup)

            # l0: base files: basePathMJDSIM (mjdsim: hardwareComponent_segment_detector.root, e.g. DUCopper_A210_Z81_1010102)
            if self.cut and self.configuration and self.detector and self.decayChain and self.segment and self.branchingRatio and self.hardwareComponent and (not self.hardwareGroup):
                tmp_configuration = self.configuration
                if self.configuration == 'DS6':
                    tmp_configuration = 'All'
                pathToFile = self.basePathMJDSIM + '/' + tmp_configuration + '/bulk/' + self.hardwareComponent + '/' + self.segment + '/'
                fileName = '%s_%s_%s.root' % (self.hardwareComponent, self.segment, self.detector)
                fullPathToFile = pathToFile + fileName

            # l0: base files: basePathOutput hardwareComponent_segment_detector_cut.npy (mjdsim: hardwareComponent_segment_detector.root)
            # if self.cut and self.configuration and self.detector and self.decayChain and self.segment and self.branchingRatio and self.hardwareComponent and (not self.hardwareGroup):
            #     pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l0' + '/'
            #     fileName = '%s_%s_%s_%s' % (self.hardwareComponent, self.segment, self.detector, str(self.cut))
            #     fullPathToFile = pathToFile + fileName

            # l1: hardwareComponent_detector_decayChain_cut_configuration.npy (mjdsim: hardwareComponent_detector_decayChainCombined.root)
            if self.cut and self.configuration and self.detector and self.decayChain and (not self.segment) and (not self.branchingRatio) and self.hardwareComponent and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l1' + '/'
                fileName = '%s_%s_%s_%s_%s.npy' % (self.hardwareComponent, self.detector, self.decayChain, str(self.cut), self.configuration)
                fullPathToFile = pathToFile + fileName

            # l2: hardwareComponent_decayChain_cut_configuration (mjdsim: hardwareComponent_MJD_decayChainCombined)
            if self.cut and self.configuration and (not self.detector) and self.decayChain and (not self.segment) and (not self.branchingRatio) and self.hardwareComponent and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l2' + '/'
                fileName = '%s_%s_%s_%s.npy' % (self.hardwareComponent, self.decayChain, str(self.cut), self.configuration)
                fullPathToFile = pathToFile + fileName

            # l3: detector_decayChain_cut_configuration (mjdsim: detector_decayChainCombined)
            if self.cut and self.configuration and self.detector and self.decayChain and (not self.segment) and (not self.branchingRatio) and (not self.hardwareComponent) and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l3' + '/'
                fileName = '%s_%s_%s_%s.npy' % (self.detector, self.decayChain, str(self.cut), self.configuration)
                fullPathToFile = pathToFile + fileName

            # l4: decayChain_cut_configuration (mjdsim: MJD_decayChainCombined)
            if self.cut and self.configuration and (not self.detector) and self.decayChain and (not self.segment) and (not self.branchingRatio) and (not self.hardwareComponent) and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l4' + '/'
                fileName = '%s_%s_%s.npy' % (self.decayChain, str(self.cut), self.configuration)
                fullPathToFile = pathToFile + fileName

            # RETURN
            if(os.path.isfile(fullPathToFile)):
                return fullPathToFile
            else:
                if ('Ge' not in fileName) and ('_Z0_' in fullPathToFile): # avoid printing expected missing files
                    return None
                if ('Ge' in fileName) and ('_2v_' in fileName): # avoid printing expected missing files
                    self.Print(0, 'Error', '  GetReadPath: No case matching this data', fullPathToFile)
                    self.Print(0, '  Warning', '  GetReadPath: Is this b/c processing only detectors of one enrichment type?')
                    return None
                else:
                    self.Print(0, 'Error', '  GetReadPath: No case matching this data', fullPathToFile)
                    return None

        def GetWritePath(self):
            """
            Get the full path for where to put a file. Many variants based on what weightFuncs are on or off or what level of loop you're in
            """
            self.UpdateSelfCurrentVars()

            self.Print(3, 'Degug', '  cVs:',self.cut, self.configuration, self.detector, self.decayChain, self.segment, self.branchingRatio, self.hardwareComponent, self.hardwareGroup)

            fullPathToFile = ''

            # hardwareComponent_segment_detector_cut (mjdsim: hardwareComponent_segment_detector)
            if self.cut and self.configuration and self.detector and self.decayChain and self.segment and self.branchingRatio and self.hardwareComponent and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l0' + '/'
                fileName = '%s_%s_%s_%s' % (self.hardwareComponent, self.segment, self.detector, str(self.cut))
                fullPathToFile = pathToFile + fileName

            # hardwareComponent_detector_decayChain_cut_configuration (mjdsim: hardwareComponent_detector_decayChainCombined)
            if self.cut and self.configuration and self.detector and self.decayChain and (not self.segment) and (not self.branchingRatio) and self.hardwareComponent and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l1' + '/'
                fileName = '%s_%s_%s_%s_%s' % (self.hardwareComponent, self.detector, self.decayChain, str(self.cut), self.configuration)
                fullPathToFile = pathToFile + fileName

            # hardwareComponent_decayChain_cut_configuration (mjdsim: hardwareComponent_MJD_decayChainCombined)
            if self.cut and self.configuration and (not self.detector) and self.decayChain and (not self.segment) and (not self.branchingRatio) and self.hardwareComponent and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l2' + '/'
                fileName = '%s_%s_%s_%s' % (self.hardwareComponent, self.decayChain, str(self.cut), self.configuration)
                fullPathToFile = pathToFile + fileName

            # detector_decayChain_cut_configuration (mjdsim: detector_decayChainCombined)
            if self.cut and self.configuration and self.detector and self.decayChain and (not self.segment) and (not self.branchingRatio) and (not self.hardwareComponent) and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l3' + '/'
                fileName = '%s_%s_%s_%s' % (self.detector, self.decayChain, str(self.cut), self.configuration)
                fullPathToFile = pathToFile + fileName

            # decayChain_cut_configuration (mjdsim: MJD_decayChainCombined)
            if self.cut and self.configuration and (not self.detector) and self.decayChain and (not self.segment) and (not self.branchingRatio) and (not self.hardwareComponent) and (not self.hardwareGroup):
                pathToFile = self.basePathOutput + '/' + str(self.configuration) + '/' + ('cut%d' % self.cut) + '/' + 'l4' + '/'
                fileName = '%s_%s_%s' % (self.decayChain, str(self.cut), self.configuration)
                fullPathToFile = pathToFile + fileName

            # RETURN
            if fullPathToFile != '':
                return fullPathToFile
            else:
                self.Print(0, 'Error', '  GetWritePath: No case matching this data', fullPathToFile)
                return None

        def GetData(self):
            """
            Get the file and return an object that is useable
            """

            fullPathToFile = self.GetReadPath()
            if fullPathToFile != None:
                cvDict = self.bscv.GetCurrentVarsDict()
                if self.basePathMJDSIM in fullPathToFile:
                    return self.bspr.GetBinnedData(inFile = fullPathToFile, **cvDict)
                if self.basePathOutput in fullPathToFile:
                    self.Print(3, 'Debug', '  Pulling data from .npy file: np.sum() =', np.sum(np.load(fullPathToFile))) #  debug
                    return np.load(fullPathToFile)
            else:
                return None

        def Save(self, data, sDat = False, sFig = False):
            """
            Save file
            """
            self.Print(3, 'Debug', '  Hist integral np.sum(data) =', np.sum(data))

            # MAKE THE PLOT
            if sFig == True:
                xArray = np.arange(self.bspr.xmin + 0.5, self.bspr.xmax + 0.5) # to be used as list of bin edges (np treats last number as INCLUDED upper edge of last been)
                plt.clf() # clear current figure to prevent any previous figures or axes from persisting
                plt.step(xArray, data, where = 'mid', color = self.GetColor())
                if np.sum(data) > 0:
                    plt.yscale('log')#, nonposy='clip')
                plt.xlim(self.bspr.xmin, self.bspr.xmax)

            # DO THE SAVING
            fileName = self.GetWritePath()
            if self.GetWritePath() != None:
                if sDat == True:
                    fileName = self.GetWritePath() # numpy will automatically append .npy
                    if(os.path.isfile(fileName + '.npy')):
                        self.Print(2, '  Save: Data already saved. Not saving.')
                    else:
                        self.Print(2, '  Saving data', fileName + '.npy')
                        np.save(fileName, data, allow_pickle = False) # numpy will automatically append .npy
                if sFig == True:
                    fileName = fileName + '.pdf'
                    if(os.path.isfile(fileName)):
                        self.Print(2, '  Save: Figure already saved. Not saving.')
                    else:
                        self.Print(2, '  Saving figure', fileName)
                        plt.savefig(fileName)
            else:
                self.Print(0, 'Error', '  Save: GetWritePath is None. Not saving.')

        def GetColor(self):
            """
            Get the color for a plot based on the current decayChain var
            """
            self.UpdateSelfCurrentVars()
            colorDict = {
                                    'Th': 'tab:brown',
                                    'U': 'tab:green',
                                    'Rn': 'tab:red',
                                    'Pb': 'tab:orange',
                                    'Co': 'tab:blue',
                                    'K': 'tab:olive',
                                    '0v': 'tab:gray',
                                    '2v': 'tab:gray'
                                    }
            return colorDict[self.decayChain]

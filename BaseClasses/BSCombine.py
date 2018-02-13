"""
A class to facilitate combination of sim results
"""

import numpy as np

class BSCombine():
        """
        A class to facilitate combination of sim results
        """
        def __init__(self, weightFunc, BSCurrentVarsObject, BSConfigDataObject):
            self.weightFunc = weightFunc
            self.bscv = BSCurrentVarsObject # The global BSCurrentVars object
            self.bscd = BSConfigDataObject # The BSConfigData object

            self.cut = None
            self.configuration = None
            self.detector = None
            self.decayChain = None
            self.segment = None
            self.branchingRatio = None
            self.hardwareComponent = None
            self.hardwareGroup = None

            self.combinedData = np.zeros(10000)
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

        def Add(self, data):
            """
            Add 'obj' to 'into' according to weight expressed in 'comboRule'
            """
            weight = self.GetWeight(self.weightFunc)
            print('  Adding hist with weight ' + self.weightFunc + ' = ' + str(weight))
            self.combinedData = self.combinedData + data*weight
            return None

        def GetCombinedData(self):
            print('  np.sum(combinedData) =', np.sum(self.combinedData))
            return self.combinedData

        def GetWeight(self, weightFunc):
            self.UpdateSelfCurrentVars()

            if weightFunc == 'One':
                return 1
            elif weightFunc == 'BranchingRatio':
                return self.branchingRatio
            elif weightFunc == 'TotalMass':
                activeDetectorMassList = self.bscd.GetActiveDetectorMassList
                return 1/np.sum(activeDetectorMassList)
            elif weightFunc == 'ActivityPerDetector':
                dCActStr = self.bscv.GetCurrentVar('decayChain') + 'Activity'
                hwCStr = self.bscv.GetCurrentVar('hardwareComponent')
                dStr = self.bscv.GetCurrentVar('detector')
                dIndex = self.bscd.GetDetectorList().index(dStr)
                dMass = self.bscd.GetDetectorMassList()[dIndex]
                activity_hwC_dC = self.bscd.GetHardwareComponentDict()[hwCStr][dCActStr][0]
                secs_per_year = self.bscd.GetSecsPerYear()
                return (activity_hwC_dC * secs_per_year)/dMass
            else:
                print('  GetWeight: weightFunc not recognized')

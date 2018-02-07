"""
A class to facilitate combination of sim results
"""

import numpy as np

class BSCombine():
        """
        A class to facilitate combination of sim results
        """
        def __init__(self, weightFunc, bscv, bscd):
            self.weightFunc = weightFunc
            self.bscv = bscv
            self.bscd = bscd
            self.combinedData = np.zeros(10000)
            return None

        def Add(self, data):
            """
            Add 'obj' to 'into' according to weight expressed in 'comboRule'
            """
            print('  adding current hist')
            weight = self.GetWeight(weightFunc)
            self.combinedData = self.combinedData + data*weight
            return None

        def GetCombinedData(self):
            return self.combinedData

        def GetWeight(self, weightFunc):
            cvDict = self.bscv.GetCurrentVarsDict()
            cut = cvDict['cut']
            configuration = cvDict['configuration']
            detector = cvDict['detector']
            decayChain = cvDict['decayChain']
            segment = cvDict['segment']
            branchingRatio = cvDict['branchingRatio']
            hardwareComponent = cvDict['hardwareComponent']
            hardwareGroup = cvDict['hardwareGroup']

            if weightFunc == 'One':
                return 1

            if weightFunc == 'BranchingRatio':
                return branchingRatio

            if weightFunc == 'TotalMass':
                activeDetectorMassList = []
                for i in range(len(self.bscd.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')])):
                    if self.bscd.GetActiveDetectorDict()[self.bscv.GetCurrentVar('configuration')][i] == 1:
                        activeDetectorMassList.append(self.bscd.GetDetectorMassList()[i])
                return 1/np.sum(activeDetectorMassList)

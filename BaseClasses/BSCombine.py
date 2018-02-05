"""
A class to facilitate combination of sim results
"""

import numpy as np

class BSCombine():
        """
        A class to facilitate combination of sim results
        """
        def __init__(self, weightFunc):
            self.weightFunc = weightFunc
            self.combinedData = np.zeros(10000)
            return None

        def Add(self, data):
            """
            Add 'obj' to 'into' according to weight expressed in 'comboRule'
            """
            print('  adding current hist')
            weightFunc = 1.
            self.combinedData = self.combinedData + data*weightFunc
            return None

        def GetCombinedData(self):
            return self.combinedData

"""
Class to store current variables and settings.
"""

class BSCurrentVars():
    """
    Class to store current variables and settings.
    """
    def __init__(self):
        self.currentVarsDict = {
                'cut': None,
                'configuration': None,
                'detector': None,
                'decayChain': None,
                'segment': None,
                'branchingRatio': None,
                'hardwareComponent': None,
                'hardwareGroup': None
                }
        return None

    def SetCurrentVar(self, objType, val):
        self.currentVarsDict[objType] = val

    def ResetCurrentVar(self, objType):
        self.currentVarsDict[objType] = None

    def GetCurrentVar(self, objType):
        return self.currentVarsDict[objType]

    def GetCurrentVarsDict(self):
        return self.currentVarsDict

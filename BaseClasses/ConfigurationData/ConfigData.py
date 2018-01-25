"""
Data on configurations, model types, etc.
"""

class ConfigData():
    def __init__(self):
        return None

    detectorList = ['D1', 'D2', 'D3', 'D4', 'D5']
    decayChainList = ['U', 'Th', 'K', 'Co', '2v']
    decayChainSegmentBranchingRatioDict = {
                            'U': {
                                'U1': 1.0,
                                'U2-0': 0.8,
                                'U2-1': 0.2,
                                'U3': 1.0
                                },
                            'Th': {
                                'Th1': 1.0,
                                'Th2': 1.0,
                                'Th3': 1.0
                                },
                            'K': {
                                'K1': 1.0
                                },
                            'Co': {
                                'Co1': 1.0
                                },
                            '2v': {
                                '2v1': 1.0
                                }
                            }
    hardwareComponentList = ['H1', 'H2']

if __name__ == '__main__':
    ConfigData()

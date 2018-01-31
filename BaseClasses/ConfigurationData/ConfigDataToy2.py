"""
Data on configurations, model types, etc.
ConfigDataToy2 holds abbreviated versions of all the real config data.
This is convenient, so that we can test the implementation of all categories of
information without looping through tons of options.
"""

class ConfigData():
    def __init__(self):
        return None

    # List of configurations
    #
    configurationList = ['All', 'DS0', 'DS1']

    # Mask for active detectors (1)
    #
    M1_activeDetectorDict = {
        'All':[	1, 1, 1, 1], #C1P1

        'DS0':[	1, 1, 1, 1], #C1P1

        'DS1':[	0, 1, 1, 1] #C1P1
    }
    M2_activeDetectorDict = {
        'All':[	1, 1, 1, 1], #C2P1

        'DS0':[	0, 0, 0, 0], #C2P1

        'DS1':[	0, 0, 0, 0] #C2P1
    }
    # Combine the two dictionaries together into a single one with the enabled detector lists concatenated
    activeDetectorDict = {}
    # for config, dets in M1_activeDetectorDict.iteritems():
    # 	activeDetectorDict[config] = dets
    # for config, dets in M2_activeDetectorDict.iteritems():
    # 	activeDetectorDict[config] += dets

    # Detector simulation names (Ge_C_P_D)
    # BSConfigData.py::GetDetectorList()
    M1_detectorList = ['1010101', '1010102', '1010103', '1010104'] #C1P1
    M2_detectorList = ['1020101', '1020102', '1020103', '1020104'] #C2P1
    detectorList = M1_detectorList + M2_detectorList

    # Detector active masses in kg
    #
    M1_detectorMassList = [0.5527, 1.0392, 0.9022, 1.0323] #C1P1
    M2_detectorMassList = [0.6382, 0.6845, 0.9692, 1.0259] #C2P1
    detectorMassList = M1_detectorMassList + M2_detectorMassList

    # Mask for enriched detectors (1)
    #
    M1_enrichedDetectorList = [1, 1, 1, 1] #C1P1
    M2_enrichedDetectorList = [0, 1, 1, 1] #C2P1
    enrichedDetectorList = M1_enrichedDetectorList + M2_enrichedDetectorList

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
    hardwareGroupList = ['CuParts', 'Near', 'Far']

if __name__ == '__main__':
    ConfigData()

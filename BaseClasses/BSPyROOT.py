"""
Class that interfaces with the mjdsim results and ROOT objects.
This class should be able to convert root into pandas or numpy objects and return them
"""

from ROOT import TFile, TCanvas, TH1D, gPad, gApplication
import numpy as np
import matplotlib.pyplot as plt

class BSPyROOT():
    def __init__(self):
        self.cut = None
        self.configuration = None
        self.detector = None
        self.decayChain = None
        self.segment = None
        self.branchingRatio = None
        self.hardwareComponent = None
        self.hardwareGroup = None

        self.nBinsX = 10000
        self.xmin = 0.0 # low edge, included
        self.xmax = 10000.0 # upper edge, excluded

        return None

    def GetBinnedData(self, inFile, **currentVarsDict):

        cvDict = currentVarsDict
        cut = cvDict['cut']
        configuration = cvDict['configuration']
        detector = cvDict['detector']
        decayChain = cvDict['decayChain']
        segment = cvDict['segment']
        branchingRatio = cvDict['branchingRatio']
        hardwareComponent = cvDict['hardwareComponent']
        hardwareGroup = cvDict['hardwareGroup']

        f = TFile(inFile, 'READ')
        c = f.Get('c1')
        hName = 'h' + str(cut)
        h = c.GetPrimitive(hName)
        hArray = np.frombuffer(h.GetArray(), dtype = 'float', count = self.nBinsX, offset = 0) # getting array of data from PyDoubleBuffer object
        xArray = np.arange(self.xmin, self.xmax + 1) # to be used as list of bin edges (np treats last number as INCLUDED upper edge of last been)

        fig, (ax) = plt.subplots(nrows = 2, ncols = 1)
        ax.step(xArray, hArray, where = 'post', color='k')
        ax.set_yscale('log', nonposy='clip')
        #ax.set_xlim(0, 3000)

        figName = '%s_%s_%s_%s.pdf' % (hardwareComponent, segment, detector, str(cut))
        print('  saving figure', figName)
        plt.savefig(figName)

        return None

# NOTES
    # where : [ ‘pre’ | ‘post’ | ‘mid’ ]
    # If ‘pre’ (the default), the interval from x[i] to x[i+1] has level y[i+1].
    # If ‘post’, that interval has level y[i].
    # If ‘mid’, the jumps in y occur half-way between the x-values.

    # For all histogram types: nbins, xlow, xup:
    # bin = 0;       underflow bin
    # bin = 1;       first bin with low-edge xlow INCLUDED
    # bin = nbins;   last bin with upper-edge xup EXCLUDED
    # bin = nbins+1; overflow bin
    #
    # root [27] h->GetXaxis()->GetBinLowEdge(1)
    # (double) 0.0000000
    # root [28] h->GetXaxis()->GetBinUpEdge(1)
    # (double) 1.0000000
    # root [29] h->GetXaxis()->GetBinUpEdge(10000)
    # (double) 10000.000
    # root [30] h->GetXaxis()->GetBinLowEdge(10000)
    # (double) 9999.0000

   # FILES LIKE: DUCopper_A210_Z81_1010102.root:
   # KEY: TCanvas  c1;1    A canvas
   # OBJ: TH1D    h1      Bellows:A210_Z81:1010102 : 1 at: 0x26b1cf0
   # OBJ: TH1D    h2      Granularity : 1 at: 0x2758620
   # OBJ: TH1D    h3      Gran+PSA : 1 at: 0x276c3d0

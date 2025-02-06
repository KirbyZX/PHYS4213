from music21 import stream, graph
from colours import Viridis as V
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


def plotHistogram(sampleset: pd.DataFrame, filename: str = None) -> None:
    '''
    Plots the histogram of a sampleset.
    '''

    plt.figure(figsize=(6,4))
    N, _, patches = plt.hist(sampleset["energy"], bins=500, log=True)

    norm = mpl.colors.LogNorm(1, N.max())
    for thisfrac, thispatch in zip(N, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    plt.xlabel("Energy")
    plt.ylabel("Count")
    #plt.xscale("symlog", linthresh=20, linscale=0.1)
    #plt.xlim(-30,0)
    #plt.xticks([-30,-20,-10,0])
    plt.show()
    
    if filename is not None:
        plt.savefig(f"..\Figures\{filename}.pdf", pad_inches=0, bbox_inches="tight")

def plotBoundaryStrength(stream: stream.Stream, threshold: float) -> None:
    '''
    Plots the boundary strengths of a stream.
    '''

    plotS = graph.plot.Scatter(stream, marker="o")

    plotS.axisX = graph.axis.OffsetAxis(plotS, 'x')
    plotS.axisY = BoundaryStrengthAxis(plotS, 'y')
    plotS.title = ""
    plotS.figureSize = (6,4)

    plotS.alpha = 1
    plotS.colors = [c.value for c in V]
    plotS.labelFontSize = 11
    plotS.tickFontSize = 10
    plotS.doneAction = None
    plotS.axisX.label = "Measure"
    plotS.hideYGrid = True

    plotS.run()

    line = plt.hlines(threshold, 0, stream.quarterLength, linestyles=":", colors="black")
    plotS.subplot.add_artist(line)
    plotS.subplot.set_xlim(left=0, right=stream.quarterLength)
    plotS.subplot.set_ylim(bottom=0, top=1)

    plotS.write()
    plt.show()

class BoundaryStrengthAxis(graph.axis.Axis):
    labelDefault = 'Boundary strength'

    def __init__(self, client=None, axisName='y'):
        super().__init__(client, axisName)
        self.minValue = 0
        self.maxValue = 1

    def ticks(self):
        newTicks = [(0,0), (1,1)]
        return newTicks

    def extractOneElement(self, el, formatDict):
        if hasattr(el, 'boundaryStrength'):
            return el.boundaryStrength
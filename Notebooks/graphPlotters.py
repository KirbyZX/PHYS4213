from music21 import *
from colours import Viridis as V
import matplotlib.pyplot as plt
from boundaryDetection import identifyBoundaries


def plotBoundaryStrength(stream: stream.Stream, threshold: float, weightings: tuple[float]) -> None:
    '''
    Plots the boundary strengths of a stream.
    '''

    boundaries = identifyBoundaries(stream, threshold, weightings)

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
        ticks = super().ticks()
        tickValues = [0,1]
        newTicks = [(0,0), (1,1)]
        return newTicks

    def extractOneElement(self, el, formatDict):
        if hasattr(el, 'boundaryStrength'):
            return el.boundaryStrength
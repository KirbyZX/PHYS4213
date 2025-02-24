from music21 import stream, graph
from colours import Viridis as V
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import re


def plotArrangement(sample: dict, phrases: list, instruments: dict):
    '''
    Create an arrangement score from a sample
    '''

    parts = {}
    for col, inst in instruments.items():
        part = stream.Part()
        part.append(inst())
        parts[col] = part

    chosen = extractChosen(sample)

    for phrase in [phrase for part in phrases for phrase in part]:
        if phrase.id in chosen:
            parts[chosen[phrase.id]].mergeElements(phrase.notes.stream()) # Focus on JUST NOTES for now 

    arrangement = stream.Score(parts.values())
    arrangement.show("midi")
    arrangement.show()

def plotSample(sample: dict, G: nx.Graph, phrases: list) -> None:
    '''
    Plots a sample as a graph.
    '''

    chosen = extractChosen(sample)

    plt.figure(0)
    pos = nx.spring_layout(G, k=0.5, seed=8)
    #nx.draw_networkx_edges(G, pos, width=0.2)
    #nx.draw_networkx_nodes(G, pos, nodelist=chosen.keys(), node_color=chosen.values(), node_size=15)

    plt.figure(1, figsize=(12,6))

    for node in G.nodes():
        if node in chosen:
            G.nodes[node]["colour"] = chosen[node]
        else:
            G.nodes[node]["colour"] = "black"
    pos = nx.multipartite_layout(G, "colour", "horizontal", 2)

    nx.draw_networkx_nodes(G, pos, node_color=[G.nodes[node]["colour"] for node in G.nodes()], node_size=[10*(p.entropy+.1) for p in phrases])
    nx.draw_networkx_edges(G, pos, width=[d["weight"]/10 for _, _, d in G.edges.data()])
    plt.show()
    #plt.savefig(f"../Figures/{identifier}_colouredGraph.pdf", pad_inches=0, bbox_inches="tight")

def extractChosen(sample: dict) -> dict:
    '''
    Extract the chosen phrases from a sample in the form "phrase": "colour".
    '''

    processNode = lambda node : re.match(r"(.*_\d+)_(\w+)", node).groups()
    return {processNode(x)[0]:processNode(x)[1] for x in sample if sample[x] == 1}

def plotHistogram(sampleset: pd.DataFrame, filename: str = None) -> None:
    '''
    Plots the histogram of a sampleset.
    '''

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
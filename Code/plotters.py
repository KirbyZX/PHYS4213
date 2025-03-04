from music21 import stream, graph, instrument
from colours import Viridis as V
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import re
import numpy as np


def plotCSV(filepath: str, xaxis: str, yaxis: str, labels: list) -> None:

    data = pd.read_csv(filepath)

    means = []
    stderr = []

    for l in labels:
        query = data.query(f"`{xaxis}` == {l}")[yaxis]
        means.append(np.mean(query))
        stderr.append(np.std(query)/np.sqrt(len(query)))

    plt.errorbar(labels, means, yerr=stderr, fmt='o')
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.show()

def plotArrangement(sample: dict, phrases: list, instruments: dict):
    '''
    Create an arrangement score from a sample
    '''

    parts = {}
    for col, inst in instruments.items():
        part = stream.Part()
        part.append(getattr(instrument, inst)())
        parts[col] = part

    chosen = extractChosen(sample)

    for phrase in [phrase for part in phrases for phrase in part]:
        if phrase.id in chosen:
            parts[chosen[phrase.id]].mergeElements(phrase.notes.stream()) # Focus on JUST NOTES for now 

    arrangement = stream.Score(parts.values())
    arrangement.show("midi")
    arrangement.show()

def plotSampleGraph(sample: dict, G: nx.Graph) -> None:
    '''
    Plots a sample as a graph.
    '''

    #plt.figure(0)
    #pos = nx.spring_layout(G, k=0.5, seed=8)
    #nx.draw_networkx_edges(G, pos, width=0.2)
    #nx.draw_networkx_nodes(G, pos, nodelist=chosen.keys(), node_color=chosen.values(), node_size=15)

    annotated = annotateSampleGraph(sample, G)

    plt.figure(1, figsize=(12,6))
    pos = nx.multipartite_layout(annotated, "colour", "horizontal", 2)

    nx.draw_networkx_nodes(annotated, pos, node_color=[annotated.nodes[node]["colour"] for node in annotated.nodes()], node_size=[10*(e[1]+.1) for e in annotated.nodes.data("entropy")])
    nx.draw_networkx_edges(annotated, pos, width=[d["weight"]/10 for _, _, d in annotated.edges.data()])

def annotateSampleGraph(sample: dict, G: nx.Graph) -> nx.Graph:
    '''
    Annotates a sample graph with the chosen phrases.
    '''

    chosen = extractChosen(sample)
    for node in G.nodes():
        if node in chosen:
            G.nodes[node]["colour"] = chosen[node]
        else:
            G.nodes[node]["colour"] = "black"

    return G

def extractChosen(sample: dict) -> dict:
    '''
    Extract the chosen phrases from a sample in the form "phrase": "colour".
    '''

    processNode = lambda node : re.match(r"(.*_\d+)_(\w+)", node).groups()
    return {processNode(x)[0]:processNode(x)[1] for x in sample if sample[x] == 1}

def plotHistogram(sampleset: pd.DataFrame) -> None:
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

def plotBoundaryStrength(stream: stream.Stream, threshold: float, filepath: str = None) -> None:
    '''
    Plots the boundary strengths of a stream.
    '''

    plotS = graph.plot.Scatter(stream, marker="o", markersize=4)

    plotS.axisX = graph.axis.OffsetAxis(plotS, 'x')
    plotS.axisY = BoundaryStrengthAxis(plotS, 'y')
    plotS.title = ""

    plotS.alpha = 1
    plotS.doneAction = None
    plotS.colors = [V.TURQUOISE.value]
    plotS.axisX.label = "Bar number"
    plotS.tickColors = "white"
    #plotS.axisX.ticks= [(m,m) for m in len(stream.getElementsByClass(stream.Measure)) if m % 4 == 0]
    plotS.hideXGrid = True
    plotS.hideYGrid = True
    plotS.figureSize = (6,3)

    plotS.run()

    line = plt.hlines(threshold, 0, stream.quarterLength, linestyles=":", colors="white")
    plotS.subplot.add_artist(line)
    plotS.subplot.set_xlim(left=0, right=stream.quarterLength)
    plotS.subplot.set_ylim(bottom=0, top=1)

    plotS.write()
    plt.show()

    if filepath is not None:
        plotS.write(filepath)

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
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import re
import numpy as np


def plotCSV(filepath: str, xaxis: str, yaxis: str, label: str = "") -> None:

    data = pd.read_csv(filepath)
    range = data[xaxis].unique()

    means = []
    stderr = []

    for r in range:
        query = data.query(f"`{xaxis}` == {r}")[yaxis]
        means.append(np.mean(query))
        stderr.append(np.std(query)/np.sqrt(len(query)))

    plt.errorbar(range, means, yerr=stderr, fmt='o', label=label)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)

def plotSampleGraph(sample: dict, G: nx.Graph, instruments: dict) -> None:
    '''
    Plots a sample as a graph.
    '''

    #plt.figure(0)
    #pos = nx.spring_layout(G, k=0.5, seed=8)
    #nx.draw_networkx_edges(G, pos, width=0.2)
    #nx.draw_networkx_nodes(G, pos, nodelist=chosen.keys(), node_color=chosen.values(), node_size=15)

    annotated = annotateSampleGraph(sample, G)

    plt.figure(1, figsize=(12,6))
    pos = nx.multipartite_layout(annotated, "assignment", "horizontal", 2)

    colours = [instruments[a]["colour"] if a != "None" else "black" for (_, a) in annotated.nodes(data="assignment")]
    entropies = [e for (_, e) in annotated.nodes(data="entropy")]

    nx.draw_networkx_nodes(annotated, pos, node_color=colours, node_size=[10*(e+.1) for e in entropies])
    nx.draw_networkx_edges(annotated, pos, width=[d["weight"]/10 for _, _, d in annotated.edges.data()])

def annotateSampleGraph(sample: dict, G: nx.Graph) -> nx.Graph:
    '''
    Annotates a sample graph with the chosen phrases.
    '''

    chosen = extractChosen(sample)
    for node in G.nodes():
        if node in chosen:
            G.nodes[node]["assignment"] = chosen[node]
        else:
            G.nodes[node]["assignment"] = "None"

    return G

def extractChosen(sample: dict) -> dict:
    '''
    Extract the indices chosen phrases from a sample in the form `{("Instrument", "Phrase number"): "Assignment"}`.
    '''

    processNode = lambda node : re.match(r"(.*)_(\d+)_(.+)", node).groups()
    # ("Instrument", Phrase number): "Assignment"
    return {(processNode(x)[0], int(processNode(x)[1])): processNode(x)[2] for x in sample if sample[x] == 1}

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

def plotBoundaryStrength(df: pd.DataFrame, threshold: float) -> None:
    '''
    Plots the boundary strengths of a stream.
    '''

    plt.scatter(df["Offset"], df["Strength"], s=1)
    plt.hlines(threshold, 0, df["Offset"].max(), linestyles="dashed")

    plt.xlim(0, df["Offset"].max())
    plt.ylim(0,1)
    plt.xlabel("Offset")
    plt.ylabel("Boundary strength")
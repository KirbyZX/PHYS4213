import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def totalEntropy(G: nx.Graph) -> float:
    '''
    Finds the total entropy of chosen nodes.
    '''

    return sum([d["entropy"] for _, d in G.nodes.data() if d["colour"] != "black"])

def findOverlaps(G: nx.Graph) -> int:
    '''
    Finds the number of adjacent chosen nodes with the same colour.
    '''

    overlaps = 0
    for (n1, n2) in G.edges:
        if G.nodes[n1]["colour"] == G.nodes[n2]["colour"] and G.nodes[n1]["colour"] != "black":
            overlaps += 1
    return overlaps

def recordSample(filepath, sample, reads) -> None:

    new_row = pd.DataFrame({
        "Total reads": [reads],
        "Chain strength": [sample.info["embedding_context"]["chain_strength"]],
        "Anneal time": [sample.info["timing"]["qpu_anneal_time_per_sample"]],
        "QPU time": [sample.info["timing"]["qpu_access_time"]],
        "Lowest energy": [sample.first.energy],
        "Chain break fraction": [sample.first.chain_break_fraction]
        })

    new_row.to_csv(filepath, index=False, mode="a", header=False)

def plotCSV(filepath: str, xaxis: str, yaxis: str, labels: list) -> None:

    data = pd.read_csv(filepath)

    means = []
    stddev = []

    for l in labels:
        means.append(np.mean(data.query(f"`{xaxis}` == {l}")[yaxis]))
        stddev.append(np.std(data.query(f"`{xaxis}` == {l}")[yaxis]))

    plt.errorbar(labels, means, yerr=stddev, fmt='o')
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.show()
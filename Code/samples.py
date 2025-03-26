import re
import networkx as nx
import itertools as iter

from dimod import SampleSet


def firstValid(sampleset: SampleSet, G: nx.Graph):
    '''
    Picks the lowest energy sample that breaks no constraints.
    '''

    filtered = sampleset.filter(lambda d: duplicates(d.sample, G) + overlaps(d.sample, G) == 0)
    return filtered.first


def duplicates(sample: dict, G: nx.Graph) -> list:
    '''
    Finds the number of nodes that have been assigned more than once.
    '''
    
    pattern = r"^(.+_\d+)_.+$"
    return sum(
        1 for n in G.nodes
        if sum(sample[k] for k in sample if re.match(pattern, k).group(1) == n) > 1)

def overlaps(sample: dict, G: nx.Graph) -> int:
    '''
    Finds the number of adjacent chosen nodes with the same colour.
    '''

    chosen = extractChosen(sample)
    possibleEdges = iter.permutations(chosen, 2)

    return sum(
        1 for u,v in possibleEdges
        if (f"{u[0]}_{u[1]}",f"{v[0]}_{v[1]}") in G.edges and chosen[u] == chosen[v]
        )

def totalEntropy(sample: dict, G: nx.Graph) -> float:
    '''
    Finds the total entropy of chosen nodes.
    '''

    chosen = extractChosen(sample)
    return sum([G.nodes[f"{ind[0]}_{ind[1]}"]["entropy"] for ind in chosen])

def extractChosen(sample: dict) -> dict:
    '''
    Extract the indices chosen phrases from a sample in the form `{("Instrument", "Phrase number"): "Assignment"}`.
    '''

    processNode = lambda node : re.match(r"(.+)_(\d+)_(.+)", node).groups()
    # ("Instrument", Phrase number): "Assignment"
    return {(processNode(x)[0], int(processNode(x)[1])): processNode(x)[2] for x in sample if sample[x] == 1}
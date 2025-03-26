import re
import networkx as nx


def duplicates(sample: dict, G: nx.Graph) -> list:
    '''
    Finds the number of nodes that have been assigned more than once.
    '''
    
    pattern = r"^(.+_\d+)_.+$"
    return sum(
        1 for n in G.nodes
        if sum(sample[k] for k in sample if re.match(pattern, k).group(1) == n) > 1)


def overlaps(G: nx.Graph) -> int:
    '''
    Finds the number of adjacent chosen nodes with the same colour.
    '''

    return sum(
        1 for n1, n2 in G.edges
        if G.nodes[n1]["assignment"] == G.nodes[n2]["assignment"] and G.nodes[n1]["assignment"] != "None"
    )


def totalEntropy(G: nx.Graph) -> float:
    '''
    Finds the total entropy of chosen nodes.
    '''

    return sum([d["entropy"] for _, d in G.nodes.data() if d["assignment"] != "None"])


def extractChosen(sample: dict) -> dict:
    '''
    Extract the indices chosen phrases from a sample in the form `{("Instrument", "Phrase number"): "Assignment"}`.
    '''

    processNode = lambda node : re.match(r"(.+)_(\d+)_(.+)", node).groups()
    # ("Instrument", Phrase number): "Assignment"
    return {(processNode(x)[0], int(processNode(x)[1])): processNode(x)[2] for x in sample if sample[x] == 1}
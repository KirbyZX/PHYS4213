import re
import networkx as nx


def duplicates(sample: dict, G: nx.Graph) -> list:
    
    pattern = r"^(.+_\d+)_.+$"
    return [n for n in G.nodes if sum(sample[k] for k in sample if re.match(pattern, k).group(1) == n) > 1]

def totalEntropy(G: nx.Graph) -> float:
    '''
    Finds the total entropy of chosen nodes.
    '''

    return sum([d["entropy"] for _, d in G.nodes.data() if d["assignment"] != "None"])

def findOverlaps(G: nx.Graph) -> int:
    '''
    Finds the number of adjacent chosen nodes with the same colour.
    '''

    overlaps = 0
    for (n1, n2) in G.edges:
        if G.nodes[n1]["assignment"] == G.nodes[n2]["assignment"] and G.nodes[n1]["assignment"] != "None":
            overlaps += 1
    return overlaps
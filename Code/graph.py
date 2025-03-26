import pandas as pd
import networkx as nx
import itertools as iter
import sys
from multiprocessing import Pool


def createGraph(phrases: pd.DataFrame, cores: int, chunksize: int) -> nx.Graph:

    G = nx.Graph()
    edges = []

    iterator = iter.combinations(phrases.index, 2)
    with Pool(cores) as pool:
        for result in pool.starmap(findEdge, iter.product(iterator, [phrases]), chunksize=chunksize):
            if result is not None:
                edges.append(result)

    G.add_nodes_from([(phrases.loc[i, "ID"], {"entropy": phrases.loc[i, "Entropy"]}) for i in phrases.index])
    G.add_weighted_edges_from(edges)
    print(f"\nGraph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges created!")

    return G

def findEdge(phraseTuple: tuple, phrases: pd.DataFrame):

    p1, p2 = phraseTuple
    print(f"Checking overlap between {p1} and {p2}", end='\r', flush=True)

    hasOverlap = lambda p1, p2 : phrases.loc[p1, "Start"] < phrases.loc[p2, "End"] and phrases.loc[p2, "Start"] < phrases.loc[p1, "End"]
    
    if hasOverlap(p1, p2):
        return (phrases.loc[p1, "ID"], phrases.loc[p2, "ID"], abs(phrases.loc[p1, "Entropy"] - phrases.loc[p2, "Entropy"]))


if __name__ == '__main__':

    identifier = sys.argv[1]
    path = f"../Pickles/{identifier}/{identifier}_"
    phrases = pd.read_csv(path + "phrases.csv", index_col=[0,1])

    G = createGraph(phrases, 4, 100)

    # nx.write_network_text(G, with_labels=False)
    nx.write_graphml(G, path + "graph.graphml")
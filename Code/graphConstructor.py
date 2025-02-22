import pickle
import networkx as nx
import itertools as iter
import sys
from multiprocessing import Pool
from boundaryDetection import hasOverlap


def createGraph(phraseLists: list, cores: int, chunksize: int) -> nx.Graph:

    G = nx.Graph()
    edges = []

    iterator = iter.chain.from_iterable([iter.product(i,j) for (i,j) in iter.combinations(phraseLists, 2)])
    with Pool(cores) as pool:
        for result in pool.imap_unordered(findEdge, iterator, chunksize=chunksize):
            if result is not None:
                edges.append(result)

    G.add_nodes_from([phrase.id for part in phraseLists for phrase in part])
    G.add_weighted_edges_from(edges)
    print("\nGraph created!")

    return G

def findEdge(phraseTuple):
    p1, p2 = phraseTuple
    print(f"Checking overlap between {p1.id} and {p2.id}", end='\r', flush=True)
    if hasOverlap(p1, p2):
        return (p1.id, p2.id, abs(p1.entropy - p2.entropy))


if __name__ == '__main__':

    identifier = sys.argv[1]
    path = f"../Pickles/{identifier}/{identifier}_"
    phrases = pickle.load(open(path + "phrases.pkl", "rb"))

    G = createGraph(phrases, 4, 100)
    print("Graph created!")
    nx.write_network_text(G, with_labels=False)

    nx.write_graphml(G, path + "graph.graphml")
from music21 import *
import matplotlib.pyplot as plt
import pickle
import networkx as nx
import itertools as iter
from multiprocessing import Pool

from boundaryDetection import hasOverlap


identifier = "haydn_opus1no1_movement1"
phraseLists = pickle.load(open(f"./Pickles/{identifier}_phrases.pkl", "rb"))

cores = 4
chunksize = 100

def updateGraph(phraseTuple):
        p1, p2 = phraseTuple
        print(f"Checking overlap between {p1.id} and {p2.id}", end='\r', flush=True)
        if hasOverlap(p1, p2):
            return (p1.id, p2.id)

if __name__ == '__main__':

    G = nx.Graph()
    edges = []

    iterator = iter.chain.from_iterable([iter.product(i,j) for (i,j) in iter.combinations(phraseLists, 2)])
    with Pool(cores) as pool:
        for result in pool.imap_unordered(updateGraph, iterator, chunksize=chunksize):
            if result is not None:
                edges.append(result)

    G.add_nodes_from([phrase.id for part in phraseLists for phrase in part])
    G.add_edges_from(edges)
    pickle.dump(G, open(f"./Pickles/{identifier}_graph.pkl", "wb"))
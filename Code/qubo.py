import networkx as nx
import itertools as iter
from music21 import instrument
from dimod import BinaryQuadraticModel
import sys
import pickle
import json


def createBQM(G: nx.Graph, phrases: list, instruments: list):
    '''
    Creates a binary quadratic model for the graph colouring problem.
    '''

    bqm = BinaryQuadraticModel(vartype="BINARY")
    allPhrases = [phrase for part in phrases for phrase in part]

    # Add all vertices for each colour
    bqm.add_variables_from([(f"{phrase.id}_{i}", 0)for phrase in allPhrases for i in instruments.keys()])

    for phrase in allPhrases:
        # Each vertex coloured at most once
        bqm.add_linear_inequality_constraint([(f"{phrase.id}_{i}", 1) for i in instruments.keys()], ub=1, lagrange_multiplier=(1,1), penalization_method="unbalanced", label="One colour per vertex")
        # Maximise vertex weighting
        bqm.add_linear_from([(f"{phrase.id}_{i}", -phrase.entropy) for i in instruments.keys()])

    for u, v, d in G.edges.data():
        # Adjacent vertices have different colours
        bqm.add_quadratic_from([(f"{u}_{i}", f"{v}_{i}", 10) for i in instruments.keys()])
        # Maximise edge weighting
        bqm.add_quadratic_from([(f"{u}_{i}", f"{v}_{j}", -d["weight"]) for i,j in iter.product(instruments.keys(), repeat=2)])

    return bqm


if __name__ == "__main__":
    
    identifier = sys.argv[1]
    path = f"../Pickles/{identifier}/{identifier}_"

    G = nx.read_graphml(path + "graph.graphml")
    phrases = pickle.load(open(path + "phrases.pkl", "rb"))
    instruments = {key: getattr(instrument, value) for (key, value) in json.load(open(path + "instruments.json")).items()}

    bqm = createBQM(G, phrases, instruments)
    print("BQM created!")

    with open(path + "bqm.json", "w") as f: 
        json.dump(bqm.to_serializable(), f)
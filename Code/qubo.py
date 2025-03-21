import networkx as nx
import itertools as iter
from dimod import BinaryQuadraticModel
import sys
import pickle
import json


def createBQM(G: nx.Graph, phrases: list, instruments: list, nodeConstraintMult: float = 1, edgeConstraintMult: float = 1, roleMult: float = 1) -> BinaryQuadraticModel:
    '''
    Creates a binary quadratic model for the graph colouring problem.
    '''

    bqm = BinaryQuadraticModel(vartype="BINARY")
    allPhrases = [phrase for part in phrases for phrase in part]

    maxEntropy = max([phrase.entropy for phrase in allPhrases])
    melodyThreshold = maxEntropy * 2/3
    harmonyThreshold = maxEntropy * 1/3

    for phrase in allPhrases:

        # Each vertex coloured at most once
        if len(instruments) > 1:
            bqm.add_linear_inequality_constraint([(f"{phrase.id}_{i}", 1) for i in instruments], ub=1, lagrange_multiplier=nodeConstraintMult*maxEntropy, penalization_method="slack", label=f"{phrase.id}")
        # Maximise vertex weighting
        bqm.add_linear_from([(f"{phrase.id}_{i}", -phrase.entropy) for i in instruments])
        
        # instruments.json in the form "instrument" : "melody"
        if phrase.entropy >= melodyThreshold:
            bqm.add_linear_from([(f"{phrase.id}_{i}", -roleMult * maxEntropy) for i in instruments if instruments[i]["role"] == "melody"])
        elif phrase.entropy >= harmonyThreshold:
            bqm.add_linear_from([(f"{phrase.id}_{i}", -roleMult * maxEntropy) for i in instruments if instruments[i]["role"] == "harmony"])
        else:
            bqm.add_linear_from([(f"{phrase.id}_{i}", -roleMult * maxEntropy) for i in instruments if instruments[i]["role"] == "bass"])

    for u, v, d in G.edges.data():
        # Adjacent vertices have different colours
        bqm.add_quadratic_from([(f"{u}_{i}", f"{v}_{i}", edgeConstraintMult * maxEntropy) for i in instruments])
        # Maximise edge weighting
        bqm.add_quadratic_from([(f"{u}_{i}", f"{v}_{j}", -d["weight"]) for i,j in iter.combinations(instruments, 2)])

    return bqm


if __name__ == "__main__":
    
    identifier = sys.argv[1]
    path = f"../Pickles/{identifier}/{identifier}_"

    G = nx.read_graphml(path + "graph.graphml")
    phrases = pickle.load(open(path + "phrases.pkl", "rb"))
    instruments = json.load(open(path + "instruments.json"))

    bqm = createBQM(G, phrases, instruments)
    print("BQM created!")

    with open(path + "bqm.json", "w") as f: 
        json.dump(bqm.to_serializable(), f)
import networkx as nx
import itertools as iter
import pandas as pd
from dimod import BinaryQuadraticModel
import sys
import json


def createBQM(G: nx.Graph, phrases: pd.DataFrame, instruments: list, nodeConstraintMult: float = 1, edgeConstraintMult: float = 1, roleMult: float = 1) -> BinaryQuadraticModel:
    '''
    Creates a binary quadratic model for the graph colouring problem.
    '''

    bqm = BinaryQuadraticModel(vartype="BINARY")

    maxEntropy = phrases["Entropy"].max()
    leadThreshold = maxEntropy * 2/3
    rhythmThreshold = maxEntropy * 1/3

    for ind in phrases.index:

        id = phrases.loc[ind, "ID"]
        entropy = phrases.loc[ind, "Entropy"]

        # Each vertex coloured at most once
        if len(instruments) > 1:
            bqm.add_linear_inequality_constraint([(f"{id}_{i}", 1) for i in instruments], ub=1, lagrange_multiplier=nodeConstraintMult*maxEntropy, penalization_method="slack", label=f"{id}")
        # Maximise vertex weighting
        bqm.add_linear_from([(f"{id}_{i}", -entropy) for i in instruments])
        
        # instruments.json in the form "instrument" : "melody"
        if entropy >= leadThreshold:
            bqm.add_linear_from([(f"{id}_{i}", -roleMult * maxEntropy) for i in instruments if instruments[i]["role"] == "lead"])
        elif phrases.loc[ind, "Entropy"] >= rhythmThreshold:
            bqm.add_linear_from([(f"{id}_{i}", -roleMult * maxEntropy) for i in instruments if instruments[i]["role"] == "rhythm"])
        else:
            bqm.add_linear_from([(f"{id}_{i}", -roleMult * maxEntropy) for i in instruments if instruments[i]["role"] == "foundation"])

    for u, v, d in G.edges.data():
        # Adjacent vertices have different colours
        bqm.add_quadratic_from([(f"{u}_{i}", f"{v}_{i}", edgeConstraintMult * maxEntropy) for i in instruments])
        # Maximise edge weighting
        bqm.add_quadratic_from([(f"{u}_{i}", f"{v}_{j}", -d["weight"]) for i,j in iter.combinations(instruments, 2)])

    return bqm


if __name__ == "__main__":
    
    identifier = sys.argv[1]
    num = sys.argv[2]
    path = f"../Pickles/{identifier}/"

    G = nx.read_graphml(path + f"{identifier}_graph.graphml")
    phrases = pd.read_csv(path + f"{identifier}_phrases.csv", index_col=[0,1])
    instruments = json.load(open(path + f"{num}/{identifier}_{num}_instruments.json"))

    bqm = createBQM(G, phrases, instruments)
    print("BQM created!")

    with open(path + f"{num}/{identifier}_{num}_bqm.json", "w") as f: 
        json.dump(bqm.to_serializable(), f)
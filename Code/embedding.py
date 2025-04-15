import json
import pandas as pd
import networkx as nx
import sys
from minorminer import find_embedding
from dwave.system import DWaveSampler
from dimod import BinaryQuadraticModel, to_networkx_graph
from qubo import createBQM


def findEmbedding(bqm: BinaryQuadraticModel) -> dict:

    embedding = find_embedding(to_networkx_graph(bqm), DWaveSampler().to_networkx_graph(), verbose=1)
    return embedding


if __name__ == "__main__":

    IDENTIFIER = sys.argv[1]
    NUM = sys.argv[2]

    picklePath = f"../Pickles/{IDENTIFIER}/{IDENTIFIER}_"
    numPath = f"../Pickles/{IDENTIFIER}/{NUM}/{IDENTIFIER}_{NUM}_"

    G = nx.read_graphml(picklePath + "graph.graphml")
    phrases = pd.read_csv(picklePath + "phrases.csv", index_col=[0,1])
    instruments = json.load(open(numPath + "instruments.json"))

    bqm = createBQM(G, phrases, instruments)
    maxDegree = bqm.degrees(array=True).max()
    qubits = bqm.num_variables
    
    print(f"Attempting to embed {qubits} qubits with maximum degree {maxDegree}...")
    embedding = findEmbedding(bqm)
    physicalQubits = sum(len(embedding[i]) for i in embedding) 
    print(f"Embedding found using {physicalQubits} qubits!")

    with open(numPath + "embedding.json", "w") as f: 
        json.dump(embedding, f)
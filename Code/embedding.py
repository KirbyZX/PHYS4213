import json
import sys
from minorminer import find_embedding
from dwave.system import DWaveSampler
from dimod import BinaryQuadraticModel, to_networkx_graph


def findEmbedding(bqm: BinaryQuadraticModel) -> None:

    embedding = find_embedding(to_networkx_graph(bqm), DWaveSampler().to_networkx_graph(), verbose=1)
    return embedding


if __name__ == "__main__":

    identifier = sys.argv[1]
    num = sys.argv[2]
    numpath = f"../Pickles/{identifier}/{num}/{identifier}_{num}_"

    bqm = BinaryQuadraticModel.from_serializable(json.load(open(numpath + "bqm.json")))
    
    embedding = findEmbedding(bqm)
    print("Embedding found!")

    with open(numpath + "embedding.json", "w") as f: 
        json.dump(embedding, f)
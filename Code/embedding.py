import json
from minorminer import find_embedding
from dwave.system import DWaveSampler
from dimod import BinaryQuadraticModel, to_networkx_graph


def findAndSaveEmbedding(bqm: BinaryQuadraticModel, filename: str) -> None:

    embedding = find_embedding(to_networkx_graph(bqm), DWaveSampler().to_networkx_graph())
    with open(filename, "w") as f: 
        json.dump(embedding, f)
import dimod.generators
import networkx as nx
import pandas as pd

import dwave_networkx as dnx
from dwave.system import DWaveSampler, EmbeddingComposite
import dimod


def solveWeightedMIS(G: nx.Graph, weights: list[tuple] = [], num_reads: int = 100, strength_multiplier: float = 2) -> pd.DataFrame:
    
    bqm = dimod.generators.maximum_weight_independent_set(G.edges, weights, strength_multiplier=strength_multiplier)

    sampler = EmbeddingComposite(DWaveSampler())
    sampleset = sampler.sample(bqm, num_reads = num_reads)

    return sampleset.to_pandas_dataframe(True)
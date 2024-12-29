import dimod.generators
import networkx as nx
import pandas as pd

import dwave_networkx as dnx
from dwave.system import DWaveSampler, EmbeddingComposite
import dimod


def solveMIS(G: nx.Graph, num_reads: int = 100) -> pd.DataFrame:
    
    bqm = dimod.generators.maximum_independent_set(G.edges, G.nodes)

    sampler = EmbeddingComposite(DWaveSampler())
    sampleset = sampler.sample(bqm, num_reads = num_reads)

    return sampleset.to_pandas_dataframe(True)


def solveWeightedMIS(G: nx.Graph, weights: list[tuple] = [], num_reads: int = 100) -> pd.DataFrame:
    
    bqm = dimod.generators.maximum_weight_independent_set(G.edges, weights)

    sampler = EmbeddingComposite(DWaveSampler())
    sampleset = sampler.sample(bqm, num_reads = num_reads)

    return sampleset.to_pandas_dataframe(True)
import dimod
import networkx as nx
import dwave_networkx as dnx # Extension of networkx
from dwave.system import LeapHybridSampler

import matplotlib.pyplot as plt

edges = [
    (0,1),
    (2,3), (2,1), (3,1),
    (4,2),
    (5,6),
    (7,8), (7,6), (8,6),
    (9,6),
    (9,10), (9,11), (10,11), (10,6), (11,6),
    (12,10), (12,11), (12,6),
    (13,10), (13,11), (13,12),
    (14,12), (14,13), (14,15),
    (15,12), (15,13),
    (16,15), (16,14), (16,12),
    (17,16), (17,15), (17,14),
    (18,17), (18,15), (18,14),
    (20,19), (20,18), (20,17), (19,18), (19,17),
    (21,20), (21,19), (21,17),
    (25,24), (25,23), (25,22), (25,21), (24,23), (24,22), (24,21), (23,22), (23,21), (22,21)
]

G = nx.Graph()
G.add_edges_from(edges)

sampler = LeapHybridSampler()
indepNodes = dnx.maximum_independent_set(G, sampler)

# Generate a BQM
# dimod.generators.maximum_independent_set(G.edges, G.nodes) 

print(indepNodes)

pos = nx.spring_layout(G) # Force specific layout

plt.figure(0)
nx.draw_networkx(G, pos=pos)
plt.savefig("beethoven", bbox_inches='tight')

plt.figure(1)
nx.draw_networkx(G, pos=pos, nodelist=indepNodes)
plt.savefig("beethoven_mis", bbox_inches='tight')
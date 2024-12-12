import dimod
import networkx as nx
import dwave_networkx as dnx # Extension of networkx
from dwave.system import LeapHybridSampler

import matplotlib.pyplot as plt

edges = [
    (0,1),
    (0,2),
    (1,2),
    (2,3),
    (3,4),
    (3,5),
    (4,5)
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
plt.savefig("graph", bbox_inches='tight')

plt.figure(1)
nx.draw_networkx(G, pos=pos, nodelist=indepNodes)
plt.savefig("solution", bbox_inches='tight')
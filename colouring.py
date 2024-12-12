import networkx as nx
import dwave_networkx as dnx
from dwave.system import LeapHybridBQMSampler
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

sampler = LeapHybridBQMSampler()
colouring = dnx.vertex_color(G, ["r","g","b"], sampler)

pos = nx.spring_layout(G) # Force specific layout

plt.figure(0)
nx.draw_networkx(G, pos=pos)
colours = [colouring[i] for i in colouring]
nx.draw_networkx_nodes(G, pos=pos, node_color=colours)
plt.savefig("colouring", bbox_inches='tight')

print(colouring)
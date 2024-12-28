import networkx as nx
import matplotlib.pyplot as plt


def defineGraph(edges: list) -> nx.Graph:

    G = nx.Graph()
    G.add_edges_from(edges)
    
    return G

def plotGraph(G: nx.Graph, pos: dict = None, figure: int = 0, filename: str = None, nodeList: list = None) -> None:
    
    plt.figure(figure)

    if nodeList is None:
        nodeList = list(G)

    nx.draw_networkx(G, pos=pos, nodelist=nodeList)
    
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')
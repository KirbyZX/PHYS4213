import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import numpy as np

from samples import extractChosen


def plotCSV(filepath: str, xaxis: str, yaxis: str, colour, marker: str = "o", label: str = "") -> None:

    data = pd.read_csv(filepath)
    range = data[xaxis].unique()

    means = []
    stderr = []

    for r in range:
        query = data.query(f"`{xaxis}` == {r}")[yaxis]
        means.append(np.mean(query))
        stderr.append(np.std(query)/np.sqrt(len(query)))

    plt.errorbar(range, means, yerr=stderr, fmt=marker, label=label, c=colour)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)

def plotSampleGraph(sample: dict, G: nx.Graph, instruments: dict) -> None:
    '''
    Plots a sample as a graph.
    '''

    chosen = extractChosen(sample)
    nx.set_node_attributes(G, "None", "assignment")

    for index in chosen:
        G.nodes[f"{index[0]}_{index[1]}"]["assignment"] = chosen[index]

    plt.figure(1, figsize=(12,6))
    pos = nx.multipartite_layout(G, "assignment", "horizontal", 2)

    colours = [instruments[a]["colour"] if a != "None" else "black" for (_, a) in G.nodes(data="assignment")]
    entropies = np.array([e for (_, e) in G.nodes(data="entropy")])
    edgeWeights = np.array([d["weight"] for _, _, d in G.edges.data()])

    nx.draw_networkx_nodes(G, pos, node_color=colours, node_size=entropies/entropies.max() + .1)
    nx.draw_networkx_edges(G, pos, width=edgeWeights/(10*edgeWeights.max()))

def plotHistogram(sampleset: pd.DataFrame) -> None:
    '''
    Plots the histogram of a sampleset.
    '''

    N, _, patches = plt.hist(sampleset["energy"], bins=500, log=True)

    norm = mpl.colors.LogNorm(1, N.max())
    for thisfrac, thispatch in zip(N, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    plt.xlabel("Energy")
    plt.ylabel("Count")
    #plt.xscale("symlog", linthresh=20, linscale=0.1)
    #plt.xlim(-30,0)
    #plt.xticks([-30,-20,-10,0])

def plotBoundaryStrength(df: pd.DataFrame, threshold: float) -> None:
    '''
    Plots the boundary strengths of a stream.
    '''

    plt.scatter(df["Offset"], df["Strength"], s=5)
    plt.hlines(threshold, 0, df["Offset"].max(), linestyles="dashed")

    plt.xlim(0, df["Offset"].max())
    plt.ylim(0,1)
    plt.xlabel("Offset")
    plt.ylabel("Boundary strength")

def plotLagrange(df: pd.DataFrame) -> None:
    '''
    Plots a parametric plot of the two variable Lagrange parameters.
    '''

    grouped = (
        df.groupby(["Node multiplier", "Edge multiplier"])
        .mean(numeric_only=True)
        .reset_index()
    )

    grouped["Broken"] = grouped["Overlaps"] + grouped["Duplicates"]

    x = grouped["Node multiplier"].unique()
    y = grouped["Edge multiplier"].unique()

    X, Y = np.meshgrid(x, y)
    Z = grouped.pivot(index="Edge multiplier", columns="Node multiplier", values="Broken").values

    plt.figure(figsize=(8,8))
    ax = plt.axes(projection ='3d')
    ax.plot_surface(X, Y, Z)

    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.view_init(elev=15, azim=50)

    ax.set_xlim(1, x.max())
    ax.set_ylim(1, y.max())
    ax.set_zlim(0, Z.max())
    ax.set_xlabel("Vertex multiplier")
    ax.set_ylabel("Edge multiplier")
    ax.set_zlabel("Broken constraints")

    ax.contourf(X, Y, Z, zdir='x', offset=-40, cmap='coolwarm')
    ax.contourf(X, Y, Z, zdir='y', offset=40, cmap='coolwarm')
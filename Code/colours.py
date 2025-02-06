from enum import Enum
import matplotlib as mpl
import matplotlib.colors as mcolors

cmap = mpl.colormaps["viridis"]

class Viridis(Enum):
    YELLOW =    mcolors.to_hex(cmap(0.99))
    GREEN =     mcolors.to_hex(cmap(0.8))
    TURQUOISE = mcolors.to_hex(cmap(0.6))
    OCEAN =     mcolors.to_hex(cmap(0.4))
    NAVY =      mcolors.to_hex(cmap(0.2))
    PURPLE =    mcolors.to_hex(cmap(0))


class Tableau(Enum):
    BLUE = mcolors.TABLEAU_COLORS["tab:blue"]
    ORANGE = mcolors.TABLEAU_COLORS["tab:orange"]
    GREEN = mcolors.TABLEAU_COLORS["tab:green"]
    RED = mcolors.TABLEAU_COLORS["tab:red"]
    PURPLE = mcolors.TABLEAU_COLORS["tab:purple"]
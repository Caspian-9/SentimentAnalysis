"""
graphing dataclass and methods
"""

from dataclasses import dataclass
import plotly


@dataclass
class GraphingInputs:
    """
    Instance Attributes:
        - data: data to graph
        - x_axis: x axis title
        - y_axis: y axis title
        - graph_title: title of graph

    Representation Invariants:
        -
    """

    data: list[list]
    x_axis: str
    y_axis: str
    graph_title: str

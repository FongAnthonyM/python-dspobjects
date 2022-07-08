""" figure.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Standard Libraries #

# Third-Party Packages #
import plotly.graph_objects as go

# Local Packages #
from .subplot import Subplot


# Definitions #
# Classes #
class Figure(go.Figure):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(self, data=None, layout=None, frames=None, skip_invalid=False, figure=None **kwargs) -> None:
        # New Attributes #
        self.subplots: list = []

        # Object Construction #
        self.construct(data=data, layout=layout, frames=frames, skip_invalid=skip_invalid, figure=figure, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, data=None, layout=None, frames=None, skip_invalid=False, figure=None, **kwargs) -> None:
        data = figure or data  # Override the data to figure if given.
        super().__init__(data=data, layout=layout, frames=frames, skip_invalid=skip_invalid, **kwargs)

    def set_subplots(self, rows=None, cols=None, **make_subplots_args) -> "Figure":
        # Ensure there are titles for annotations
        if "subplot_titles" not in make_subplots_args:
            make_subplots_args["subplot_titles"] = [f"" for i in range(rows*cols)]

        super().set_subplots(rows=rows, cols=cols, **make_subplots_args)

        self.subplots.clear()
        self.subplots.extend([[None]*cols]*rows)
        for row in range(rows):
            for col in range(col):
                title = self.layout.annotations[(row * cols) + col]
                self.subplots[row][col] = subplot = Subplot(figure=self, row=row, col=col, title=title)

        return self

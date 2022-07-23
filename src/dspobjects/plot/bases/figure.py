""" _figure.py

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
    def __init__(self, data=None, layout=None, frames=None, skip_invalid=False, figure=None, **kwargs) -> None:
        # New Attributes #
        self._subplots: list[Subplot] = []

        # Object Construction #
        self.construct(data=data, layout=layout, frames=frames, skip_invalid=skip_invalid, figure=figure, **kwargs)

    @property
    def subplots(self):
        return self._subplots

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, data=None, layout=None, frames=None, skip_invalid=False, figure=None, **kwargs) -> None:
        data = figure or data  # Override the data to _figure if given.
        super().__init__(data=data, layout=layout, frames=frames, skip_invalid=skip_invalid, **kwargs)

    def set_subplots(self, rows=None, cols=None, **make_subplots_args) -> "Figure":
        # Ensure there are titles for annotations
        if "subplot_titles" not in make_subplots_args:
            make_subplots_args["subplot_titles"] = [f" " for i in range(rows*cols)]

        super().set_subplots(rows=rows, cols=cols, **make_subplots_args)

        self._subplots.clear()
        self._subplots.extend([None] * cols for r in range(rows))
        for row in range(rows):
            for col in range(cols):
                title = self.layout.annotations[(row * cols) + col]
                self._subplots[row][col] = Subplot(figure=self, row=row+1, col=col+1, title=title)

        return self

    def get_legendgroups(self):
        return set(trace.legendgroup for trace in self.data if trace.legendgroup is not None)

    def to_image(self, *args, rangeslider_visible=False, **kwargs):

        if not rangeslider_visible:
            self.update_xaxes(dict(rangeslider={"visible": False}))

        super().to_image(*args, *kwargs)

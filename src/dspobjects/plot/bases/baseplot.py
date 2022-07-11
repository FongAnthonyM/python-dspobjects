""" baseplot.py

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
from baseobjects import BaseObject
import plotly.graph_objects as go

# Local Packages #
from .subplot import Subplot
from .figure import Figure


# Definitions #
# Classes #
class BasePlot(BaseObject):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_layout_seetings = dict()
    default_title_settings = dict()
    default_xaxis_settings = dict()
    default_yaxis_settings = dict()
    default_trace_settings = dict()

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        init: bool = True,
    ) -> None:
        # New Attributes #
        self.new_trace_settings: dict = self.default_trace_settings.copy()
        self.new_layout_settings: dict[str, Any] = self.default_layout_seetings.copy()

        self.figure: go.Figure | None = None
        self._subplot: Subplot | None = None
        self._xaxis: go.layout.XAxis | None = None
        self._yaxis: go.layout.YAxis | None = None

        self.traces: list = []

        # Object Construction #
        if init:
            self.construct(figure=figure)
            
    @property
    def xaxis(self) -> go.layout.XAxis:
        if self._xaxis is not None:
            return self._xaxis
        elif self._subplot is not None:
            return self._subplot.xaxis
        elif self.figure is not None:
            return self.figure.layout.xaxis
        else:
            return None

    @property
    def yaxis(self) -> go.layout.YAxis:
        if self._xaxis is not None:
            return self._xaxis
        elif self.figure is not None:
            return self.figure.layout.yaxis
        else:
            return None

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
    ) -> None:
        if figure is not None and subplot is not None:
            if  subplot.figure != figure:
                raise ValueError("The figure and _subplot do match.")

        if figure is not None:
            self.figure = figure
            self.figure.update_layout(self.default_layout_seetings)
        elif self.figure is None and subplot is None:
            self.figure = Figure()
            self.figure.update_layout(self.default_layout_seetings)

        if subplot is not None:
            self._subplot = subplot
            self.figure = subplot.figure

        self.update_xaxis(self.default_xaxis_settings)
        self.update_yaxis(self.default_yaxis_settings)

    def set_subplot(self, subplot: Subplot):
        if subplot.figure != self.figure:
            raise ValueError("Cannot change plot to different figure, create new plot instead.")

        self._subplot = subplot

        for trace in self.traces:
            x_subplot = f"x{'' if (subplot.row - 1) <= 0 else (subplot.row - 1)}"
            y_subplot = f"y{'' if (subplot.col - 1) <= 0 else (subplot.col - 1)}"
            trace.update(xaxis=x_subplot, yaxis=y_subplot)

    def set_xaxis(self):
        pass

    def set_yaxis(self):
        pass

    def update_title(self, dict1=None, overwrite=False, **kwargs) -> None:
        if self._subplot is not None:
            self._subplot.title.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self.figure.layout.title.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def update_xaxis(self, dict1=None, overwrite=False, **kwargs) -> None:
        if self._subplot is not None:
            self._subplot.xaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self.figure.layout.xaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def update_yaxis(self, dict1=None, overwrite=False, **kwargs) -> None:
        if self._subplot is not None:
            self._subplot.yaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self.figure.layout.yaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def add_traces(self, traces):
        if self._subplot is not None:
            for trace in traces:
                self.traces.append(self._subplot.add_trace(trace))
        else:
            for trace in traces:
                self.figure.add_trace(trace)
                self.traces.append(self.figure.data[-1])

    def update_traces(self, dict1=None, overwrite=False, **kwargs) -> None:
        for trace in self.traces:
            trace.update(dict1=dict1, overwrite=overwrite, **kwargs)

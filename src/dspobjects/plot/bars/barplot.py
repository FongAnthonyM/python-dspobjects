""" barplot.py

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
import numpy as np
import plotly.graph_objects as go

# Local Packages #
from ...operations import iterdim
from ..bases import Subplot, BasePlot


# Definitions #
# Classes #
class BarPlot(BasePlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str ='h',
        separated: bool = False,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 5.0,
        init: bool = True,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._separated_categories: bool = False
        self._orientation: str = 'v'
        self._names = None

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                labels=labels,
                names=names,
                orientation=orientation,
                separated=separated,
                axis=axis,
                c_axis=c_axis,
                t_offset=t_offset,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str | None = None,
        separated: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
    ) -> None:
        if names is not None:
            self._names = names

        if orientation is not None:
            self._orientation = orientation

        if separated is not None:
            self._separated_categories = separated

        super().construct(
            figure=figure,
            subplot=subplot,
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
        )

        if (self._orientation == "v" and self.y is not None or
            self._orientation == "h" and self.x is not None):
            # Apply Data
            self.apply_data()

    def set_trace_color(self, trace, color):
        if isinstance(trace, int):
            trace = self._traces[trace]

        trace.update(base=dict(color=color))

    def generate_locations(self, n_locations):
        return np.arange(n_locations) * self._trace_offset

    def apply_single_bar_traces(self, data, locations, b_axis, l_axis, names):
        n_traces = data.shape[self._c_axis]
        n_additions = n_traces - len(self._traces)

        default_trace = go.Bar(**self.new_trace_settings)
        self.add_traces((default_trace,) * n_additions)

        trace_iter = iter(self._traces)
        trace_data = zip(iterdim(data, self._c_axis), trace_iter)
        for i, (bars, trace) in enumerate(trace_data):
            data = {l_axis: locations, b_axis: bars}
            trace.update(data)
            trace.name = names[0]
            trace.orientation = self._orientation
            trace.visible = True

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

    def apply_separate_bar_traces(self, data, locations, b_axis, l_axis, names):
        names = [f"[Index {i + 1}] {name}" for i, name in enumerate(names)] if self._label_index else names
        n_traces = len(data)
        n_additions = n_traces - len(self._traces)

        default_trace = go.Bar(**self.new_trace_settings)
        self.add_traces((default_trace,) * n_additions)

        trace_iter = iter(self._traces)
        for g, bars in enumerate(iterdim(data, self._c_axis)):
            for i, (bar, location, trace) in enumerate(zip(bars, locations, trace_iter)):
                data = {l_axis: [location], b_axis: [bar]}
                trace.update(data)
                trace.name = names[i]
                trace.legendgroup = trace.name
                if g > 0:
                    trace.showlegend = False
                trace.orientation = self._orientation
                trace.visible = True

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

    def apply_data(self, x=None, y=None, labels=None, names=None, orientation=None):
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if orientation is not None:
            self._orientation = orientation
        else:
            orientation = self._orientation

        if orientation == 'v':
            locations = self.x
            data = self.y
            l_axis = 'x'
            b_axis = 'y'
        elif orientation == 'h':
            locations = self.y
            data = self.x
            l_axis = 'y'
            b_axis = 'x'
        else:
            raise ValueError(f"{orientation} is not a valid orientation. [v, h]")

        n_bars = data.shape[self._axis]

        if locations is None:
            locations = self.generate_locations(n_locations=n_bars)

        if labels is None:
            if self.labels is None:
                labels = [f"Channel {i}" for i in range(1, n_bars + 1)]
            else:
                labels = self.labels
        else:
            self.labels = labels

        if self._label_index:
            if self._tick_index_only:
                tick_labels = [f"[Index {i + 1}]" for i, name in enumerate(labels)]
            else:
                tick_labels = [f"{name} [Index {i + 1}]" for i, name in enumerate(labels)]
        else:
            tick_lables = labels

        n_channels = data.shape[self._c_axis]
        if names is None:
            if self._names is None:
                names = [f"Bar Set {i}" for i in range(1, n_channels + 1)]
            else:
                namess = self.names
        else:
            self.names = names

        if self._separated_categories:
            self.apply_separate_bar_traces(data, locations, b_axis, l_axis, labels)
        else:
            self.apply_single_bar_traces(data, locations, b_axis, l_axis, names)

        tick_info = dict(
            range=[-1 * self._trace_offset, n_bars * self._trace_offset],
            tickvals=locations,
            ticktext=tick_labels,
        )

        if orientation == 'v':
            self.update_xaxis(tick_info)
        else:
            self.update_yaxis(tick_info)

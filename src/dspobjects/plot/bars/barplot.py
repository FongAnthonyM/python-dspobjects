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
from collections.abc import Iterable
from typing import Any

# Third-Party Packages #
import numpy as np
from plotly.basedatatypes import BaseTraceType
import plotly.graph_objects as go

# Local Packages #
from ...operations import iterdim
from ..bases import Figure, Subplot, BasePlot


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
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str = 'h',
        separated: bool = False,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 5.0,
        build: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._separated_categories: bool = False
        self._orientation: str = 'v'
        self._names: Iterable[str] | None = None

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
                build=build,
                **kwargs,
            )

    @property
    def separated_categories(self) -> bool:
        return self._separated_categories

    @property
    def orientation(self) -> str:
        return self._orientation

    @property
    def names(self) -> Iterable[str]:
        return self._names

    # Instance Methods #
    # Constructors/Destructors
    def _update_attributes(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str | None = None,
        separated: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        **kwargs: Any,
    ) -> None:
        if names is not None:
            self._names = names

        if orientation is not None:
            if orientation in {'v', 'h'}:
                self._orientation = orientation
            else:
                raise ValueError(f"{orientation} is not a valid orientation. [v, h]")

        if separated is not None:
            self._separated_categories = separated

        super()._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            **kwargs,
        )

    def build(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str | None = None,
        separated: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        **kwargs: Any,
    ) -> None:
        self._update_attributes(
            x=x,
            y=y,
            labels=labels,
            names=names,
            orientation=orientation,
            separated=separated,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            **kwargs,
        )

        if (self._orientation == "v" and self.y is not None or
            self._orientation == "h" and self.x is not None):
            # Apply Data
            self.update_plot()

    # Traces
    def set_trace_color(self, trace: int | BaseTraceType, color: str) -> None:
        if isinstance(trace, int):
            trace = self._traces[trace]

        trace.update(base=dict(color=color))

    def generate_locations(self, n_locations: int):
        return np.arange(n_locations) * self._trace_offset

    def apply_single_bar_traces(self, data, locations, b_axis, l_axis, names):
        # Handle Legend Groups
        if self._group_existing_legend:
            existing_group = self._figure.get_legendgroups()
        else:
            existing_group = {}

        n_traces = data.shape[self._c_axis]
        n_additions = n_traces - len(self._trace_groups["data"])

        default_trace = go.Bar()
        self.add_traces((default_trace,) * n_additions, group="data")

        trace_iter = iter(self._trace_groups["data"])
        trace_data = zip(iterdim(data, self._c_axis), trace_iter)
        for i, (bars, trace) in enumerate(trace_data):
            data = {l_axis: locations, b_axis: bars}
            trace.update(data)
            trace.name = names[i]
            if self._group_existing_legend:
                trace.legendgroup = names[i]
            if names[i] in existing_group:
                trace.showlegend = False
            trace.orientation = self._orientation
            trace.visible = True

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

    def apply_separate_bar_traces(self, data, locations, b_axis, l_axis, names):
        # Handle Legend Groups
        if self._group_existing_legend:
            existing_group = self._figure.get_legendgroups()
        else:
            existing_group = {}

        n_traces = len(data)
        n_additions = n_traces - len(self._trace_groups["data"])

        default_trace = go.Bar()
        self.add_traces((default_trace,) * n_additions, group="data")

        trace_iter = iter(self._trace_groups["data"])
        for g, bars in enumerate(iterdim(data, self._c_axis)):
            for i, (bar, location, trace) in enumerate(zip(bars, locations, trace_iter)):
                data = {l_axis: [location], b_axis: [bar]}
                trace.update(data)
                trace.name = names[i]
                trace.legendgroup = trace.name
                if g > 0 or names[i] in existing_group:
                    trace.showlegend = False
                trace.orientation = self._orientation
                trace.visible = True

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

    def update_plot(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        names: list | None = None,
        orientation: str | None = None,
        separated: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        **kwargs: Any,
    ) -> None:
        self._update_attributes(
            x=x,
            y=y,
            labels=labels,
            names=names,
            orientation=orientation,
            separated=separated,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            **kwargs,
        )

        # Prepare Data to go in the correct orientation
        if self._orientation == 'v':
            locations = self.x
            data = self.y
            l_axis = 'x'
            b_axis = 'y'
        elif self._orientation == 'h':
            locations = self.y
            data = self.x
            l_axis = 'y'
            b_axis = 'x'
        else:
            raise ValueError(f"{self._orientation} is not a valid orientation. [v, h]")

        n_bars = data.shape[self._axis]
        n_sets = data.shape[self._c_axis]

        if locations is None:
            locations = self.generate_locations(n_locations=n_bars)

        # Generate Labels
        labels = self.generate_labels(n_labels=n_bars)

        names = self.generate_names(n_names=n_sets)
        tick_labels = self.generate_tick_labels(labels=labels)

        # Apply Data to Traces
        if self._separated_categories:
            self.apply_separate_bar_traces(data, locations, b_axis, l_axis, labels)
        else:
            self.apply_single_bar_traces(data, locations, b_axis, l_axis, names)

        # Apply Labels and Range
        tick_info = dict(
            range=[-1 * self._trace_offset, n_bars * self._trace_offset],
            tickvals=locations,
            ticktext=tick_labels,
        )

        if orientation == 'v':
            self.update_xaxis(tick_info)
        else:
            self.update_yaxis(tick_info)

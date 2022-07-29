""" seriesplot.py

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
import itertools

# Third-Party Packages #
from plotly.basedatatypes import BaseTraceType
import plotly.graph_objects as go
import numpy as np

# Local Packages #
from ...operations import iterdim
from ..bases import Figure, Subplot, BasePlot


# Definitions #
# Classes #
class SeriesPlot(BasePlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_layout_settings: dict[str, Any] = BasePlot.default_layout_settings | dict(
        dragmode="zoom",
        template="plotly_white",
        margin=dict(t=50, b=50),
        modebar_add=['zoom',
                     'pan',
                     'drawline',
                     'drawopenpath',
                     'drawclosedpath',
                     'drawcircle',
                     'drawrect',
                     'eraseshape'
                     ],
    )
    default_xaxis_settings: dict[str, Any] = {}
    default_yaxis_settings: dict[str, Any] = {}
    default_trace_settings: dict[str, Any] = dict(
        mode="lines",
        line={"width": 1},
        showlegend=True,
    )

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: Iterable[str] | None = None,
        label_axis: bool = False,
        label_index: bool = True,
        tick_index_only: bool = False,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 0,
        z_score: bool = False,
        build: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._z_score: bool = False

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                labels=labels,
                label_axis=label_axis,
                label_index=label_index,
                tick_index_only=tick_index_only,
                axis=axis,
                c_axis=c_axis,
                t_offset=t_offset,
                z_score=z_score,
                build=build,
                **kwargs,
            )

    @property
    def z_score(self) -> bool:
        return self._z_score

    # Instance Methods #
    # Constructors/Destructors
    def _update_attributes(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs: Any,
    ) -> None:
        if z_score is not None:
            self._z_score = z_score

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
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs: Any,
    ) -> None:
        super().build(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            z_score=z_score,
            **kwargs,
        )

        if self.y is not None:
            self.update_plot()

    # TraceContainer
    def set_trace_color(self, trace: int | BaseTraceType, color: str) -> None:
        if isinstance(trace, int):
            trace = self._traces[trace]

        trace.update(line=dict(color=color))

    def _update_data(self, x, names, existing_legend_group) -> None:
        # Z Score Y Data
        if self.z_score:
            y_mod = (self.y - np.nanmean(self.y, axis=self._axis)) / np.nanstd(self.y, axis=self._axis)
        else:
            y_mod = self.y

        # Apply Data to TraceContainer
        if self._text is not None:
            if self.text.shape[self._c_axis] == 1:
                text_iter = itertools.repeat(np.squeeze(self._text), self.y.shape[self._c_axis])
            else:
                text_iter = iterdim(self._text, self._c_axis)
        else:
            text_iter = iterdim(y_mod, self._c_axis)

        trace_iter = iter(self._traces["data"])
        trace_data = zip(iterdim(self.y, self._c_axis), text_iter, trace_iter)
        for i, (text, plot_c, trace) in enumerate(trace_data):
            trace.x = x
            trace.y = plot_c + (i * self._trace_offset)
            trace.name = names[i]
            if self._group_existing_legend:
                trace.legendgroup = names[i]
            if names[i] in existing_legend_group:
                trace.showlegend = False
            if self.z_score:
                trace.text = [f"{c:.4f}" for c in text]
            trace.visible = True

        # Turn Off Unused TraceContainer
        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

    def update_data(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs,
    ) -> None:
        self._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            z_score=z_score,
            **kwargs,
        )
        # Handle Legend Groups
        if self._group_existing_legend:
            existing_legend_group = self._figure.get_legendgroups()
        else:
            existing_legend_group = {}

        # Data Info
        n_samples = self.y.shape[self._axis]
        n_channels = self.y.shape[self._c_axis]
        n_additions = n_channels - len(self._traces["data"])

        # Create New TraceContainer
        default_trace = go.Scattergl()
        self.add_traces((default_trace,)*n_additions, group="data")

        # Generate Labels
        labels = self.generate_labels(n_labels=n_channels)

        names = self.generate_names(names=labels)
        tick_labels = self.generate_tick_labels(labels=labels)

        # Generate X Data
        x = self.generate_x(n_samples=n_samples)

        self._update_data(x=x, names=names, existing_legend_group=existing_legend_group)

    def update_plot(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs,
    ) -> None:
        self._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            z_score=z_score,
            **kwargs,
        )
        # Handle Legend Groups
        if self._group_existing_legend:
            existing_legend_group = self._figure.get_legendgroups()
        else:
            existing_legend_group = {}

        # Data Info
        n_samples = self.y.shape[self._axis]
        n_channels = self.y.shape[self._c_axis]
        n_additions = n_channels - len(self._traces["data"])

        # Create New TraceContainer
        default_trace = go.Scattergl()
        self.add_traces((default_trace,)*n_additions, group="data")

        # Generate Labels
        labels = self.generate_labels(n_labels=n_channels)

        names = self.generate_names(names=labels)
        tick_labels = self.generate_tick_labels(labels=labels)

        # Generate X Data
        x = self.generate_x(n_samples=n_samples)

        # Update Data
        self._update_data(x=x, names=names, existing_legend_group=existing_legend_group)

        # Apply Labels and Range
        y_axis = dict()

        if self.yaxis.range is None:
            y_axis["range"] = [-1 * self._trace_offset, n_channels * self._trace_offset]

        if self._label_axis:
            y_axis["tickvals"] = np.arange(n_channels) * self._trace_offset
            y_axis["ticktext"] = tick_labels

        self.update_yaxis(y_axis)

        # Apply Range and Slider
        x_axis = dict()

        if self.xaxis.range is None:
            x_axis["range"] = dict(range=[x[0], x[-1]])

        if self.xaxis.rangeslider.visible:
            x_axis["rangeslider"] = dict(range=[float(x[0]), float(x[-1])])

        self.update_xaxis(x_axis)

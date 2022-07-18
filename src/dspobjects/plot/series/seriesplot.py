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
        legend=dict(traceorder="reversed"),
        template="plotly_white",
        margin=dict(
            t=50,
            b=50
        ),
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
    default_xaxis_settings: dict[str, Any] = dict(
        showspikes=True,
        spikemode="across",
        autorange=True,
        fixedrange=True,
        rangeslider=dict(
            autorange=False,
            thickness=0.04,
            borderwidth=1,
            yaxis=dict(rangemode="auto")
        ),
    )
    default_yaxis_settings: dict[str, Any] = dict(
        showgrid=False,
        tickmode="array",
        autorange=False,
        fixedrange=False,
        showline=True,
        ticks="",
        type="linear",
        zeroline=False,
    )
    default_trace_settings: dict[str, Any] = dict(
        mode="lines",
        line={"width": 1},
        showlegend=True,
    )
    default_hovertemplate: str | None = ("%{text} %{_y_unit}<br>" +
                                         "%{x:.4f} %{_x_unit}")

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: Iterable[str] | None = None,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 5.0,
        z_score: bool = True,
        build: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._z_score: bool = True

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                labels=labels,
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
    def construct(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        build: bool = True,
        **kwargs: Any
    ) -> None:
        super().construct(
            figure=figure,
            subplot=subplot,
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            z_score=z_score,
            **kwargs,
        )

        if build and self.y is not None:
            self.update_plot()

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

    # Traces
    def set_trace_color(self, trace: int | BaseTraceType, color: str) -> None:
        if isinstance(trace, int):
            trace = self._traces[trace]

        trace.update(line=dict(color=color))

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

        # Data Info
        n_samples = self.y.shape[self._axis]
        n_channels = self.y.shape[self._c_axis]
        n_additions = n_channels - len(self._traces)

        # Create New Traces
        default_trace = go.Scattergl(**self._trace_settings)
        self.add_traces((default_trace,)*n_additions)

        # Generate Labels
        labels = self.generate_labels(n_labels=n_channels)

        names = self.generate_names(names=labels)
        tick_labels = self.generate_tick_labels(labels=labels)

        # Generate X Data
        if self.x is None:
            x = self.generate_x(n_samples=n_samples)
        else:
            x = self.x

        # Z Score Y Data
        if self.z_score:
            y_mod = (self.y - np.nanmean(self.y, axis=self._axis)) / np.nanstd(self.y, axis=self._axis)
        else:
            y_mod = self.y

        # Apply Data to Traces
        trace_iter = iter(self._traces)
        trace_data = zip(iterdim(self.y, self._c_axis), iterdim(y_mod, self._c_axis), trace_iter)
        for i, (channel, plot_c, trace) in enumerate(trace_data):
            trace.x = np.squeeze(x)
            trace.y = plot_c + (i * self._trace_offset)
            trace.name = names[i]
            trace.text = [f"{c:.4f}" for c in channel]
            trace.visible = True

        # Turn Off Unused Traces
        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

        # Apply Labels and Range
        self.update_yaxis(dict(
            range=[-1 * self._trace_offset, n_channels * self._trace_offset],
            tickvals=np.arange(n_channels) * self._trace_offset,
            ticktext=tick_labels,
        ))

        # Apply Range and Slider
        self.update_xaxis(dict(
            range=[x[0], x[-1]],
            rangeslider=dict(range=[float(x[0]), float(x[-1])]),
        ))

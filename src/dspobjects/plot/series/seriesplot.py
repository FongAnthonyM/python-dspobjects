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

# Third-Party Packages #
import plotly.graph_objects as go
import numpy as np

# Local Packages #
from ...operations import iterdim
from ..bases import BasePlot, Figure


# Definitions #
# Classes #
class SeriesPlot(BasePlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_layout = dict(
        dragmode="zoom",
        legend=dict(traceorder="reversed"),
        template="plotly_white",
        margin=dict(
            t=50,
            b=50
        ),
        modebar_add=['drawline',
                     'drawopenpath',
                     'drawclosedpath',
                     'drawcircle',
                     'drawrect',
                     'eraseshape'
                     ],
    )
    default_xaxis_settings = dict(
        showspikes=True,
        spikemode="across",
        title=dict(
            text=x_title,
            font=dict(size=18),
        ),
        autorange=True,
        fixedrange=True,
        range=[x[0], x[-1]],
        rangeslider=dict(
            autorange=False,
            range=[x[0], x[-1]],
            yaxis=dict(rangemode="auto")
        ),
    )
    default_yaxis_settings = dict(
        anchor="free",
        autorange=False,
        mirror=True,
        showline=True,
        side="left",
        tickmode="auto",
        ticks="",
        type="linear",
        zeroline=False,
    )
    default_trace_settings = dict(
        mode="lines",
        line={"width": 1},
        showlegend=True,
    )


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
        init: bool = True,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self.axis: int = 0
        self.c_axis: int = 1
        self.trace_offset: float = 5.0
        self.z_score: bool = True

        self.x = None
        self.y = None
        self.labels = None

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
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
    ) -> None:
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if labels is not None:
            self.labels = labels

        if axis is not None:
            self.axis = axis

        if c_axis is not None:
            self.c_axis = c_axis

        if t_offset is not None:
            self.trace_offset = t_offset

        if z_score is not None:
            self.z_score = z_score

        super().construct(figure=figure, subplot=subplot)

        if self.y is not None:
            self.apply_data()

    def generate_x(self):
        return tuple(range(0, n_samples))

    def apply_data(self, x=None, y=None, labels=None):
        if y is not None:
            self.y = y

        n_channels = self.y.shape[self.c_axis]
        n_additions = n_channels - len(self.traces)

        default_trace = go.Scattergl()
        default_trace.update(self.new_trace_settings)
        self.add_traces((default_trace,)*n_additions)

        if labels is None:
            if self.labels is None:
                labels = [f"Channel {i}" for i in range(1, n_channels + 1)]
            else:
                labels = self.labels
        else:
            self.labels = labels

        if x is None:
            if self.x is None:
                x = self.generate_x()
            else:
                x = self.x
        else:
            self.x = x

        if self.z_score:
            y_mod = (self.y - np.nanmean(self.y, axis=self.axis)) / np.nanstd(self.y, axis=self.axis)
        else:
            y_mod = self.y

        trace_iter = iter(self.traces)
        for i, (channel, plot_c, trace) in enumerate(zip(iterdim(self.y, c_axis), iterdim(y_mod, c_axis), trace_iter)):
            trace.x = x
            trace.y = plot_c + (i * self.trace_offset)
            trace.name = labels[i]
            trace.text = [f"{c:.4f}" for c in channel],
            trace.visible = True

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.visible = False

""" heatmapplot.py

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
from typing import Any

# Third-Party Packages #
import numpy as np
import plotly.graph_objects as go

# Local Packages #
from ..bases import Subplot, BasePlot


# Definitions #
# Classes #
class HeatmapPlot(BasePlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_color_sequence: list | None = None

    # Magic Methods #
    # Construction/Destruction
    def __init__(
            self,
            figure: go.Figure | None = None,
            subplot: Subplot | None = None,
            x: np.ndarray | None = None,
            y: np.ndarray | None = None,
            z: np.ndarray | None = None,
            labels: list | None = None,
            names: list | None = None,
            separated: bool = False,
            axis: int = 0,
            c_axis: int = 1,
            t_offset: float = 5.0,
            init: bool = True,
            build: bool = True,
            **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._separated_bands: bool = False
        self._names = None

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                z=z,
                labels=labels,
                names=names,
                separated=separated,
                axis=axis,
                c_axis=c_axis,
                t_offset=t_offset,
                buid=build,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
            self,
            figure: go.Figure | None = None,
            subplot: Subplot | None = None,
            x: np.ndarray | None = None,
            y: np.ndarray | None = None,
            z: np.ndarray | None = None,
            labels: list | None = None,
            names: list | None = None,
            separated: bool | None = None,
            axis: int | None = None,
            c_axis: int | None = None,
            t_offset: float | None = None,
            build: bool = True,
            **kwargs: Any,
    ) -> None:
        if names is not None:
            self._names = names

        if separated is not None:
            self._separated_bands = separated

        super().construct(
            figure=figure,
            subplot=subplot,
            x=x,
            y=y,
            z=z,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            **kwargs,
        )

        if self.z is not None:
            # Apply Data
            self.apply_data()

    def set_trace_color(self, trace, color):
        if isinstance(trace, int):
            trace = self._traces[trace]

        trace.colorscale = color

    def apply_single_trace(self, x=None, y=None, z=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        z = self.z if z is None else z

        if len(self._traces) < 1:
            default_trace = go.Heatmap(**self.new_trace_settings)
            self.add_traces((default_trace,))

        trace_iter = iter(self._traces)
        trace = next(trace_iter)

        trace.update(dict(
            x=np.squeeze(x),
            y=np.squeeze(y),
            z=z,
        ))

        for trace in trace_iter:
            trace.x = None
            trace.y = None
            trace.z = None
            trace.visible = False

    def apply_separate_row_traces(self):
        pass

    def apply_data(self, x=None, y=None, labels=None):
        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if self._separated_bands:
            self.apply_separate_row_traces()
        else:
            self.apply_single_trace()

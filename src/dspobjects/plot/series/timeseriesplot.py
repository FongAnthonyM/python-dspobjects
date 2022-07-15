""" timeseriesplot.py

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
import numpy as np
import plotly.graph_objects as go

# Local Packages #
from ..bases import Subplot
from .seriesplot import SeriesPlot


# Definitions #
# Classes #
class TimeSeriesPlot(SeriesPlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_x_unit = "s"
    default_y_unit = "mV"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        sample_rate: float | None = None,
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
        self.sample_rate: float | None = None

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                sample_rate=sample_rate,
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
        sample_rate: float | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
    ) -> None:
        if sample_rate is not None:
            self.sample_rate = sample_rate

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
        )

    def generate_x(self, n_samples):
        if self.sample_rate is None:
            return tuple(range(0, n_samples))
        else:
            return np.arange(n_samples) / self.sample_rate

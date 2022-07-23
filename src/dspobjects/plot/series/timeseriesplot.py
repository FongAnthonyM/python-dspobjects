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
from typing import Any

# Third-Party Packages #
import numpy as np
import plotly.graph_objects as go

# Local Packages #
from ..bases import Figure, Subplot
from .stackedseriesplot import StackedSeriesPlot


# Definitions #
# Classes #
class TimeSeriesPlot(StackedSeriesPlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_x_unit: str | None = "s"
    default_y_unit: str | None = "mV"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: Figure | None = None,
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
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._sample_rate: float | None = None

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
                **kwargs,
            )

    @property
    def sample_rate(self) -> float | None:
        return self._sample_rate

    # Instance Methods #
    def _update_attributes(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        sample_rate: float | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        z_score: bool | None = None,
        **kwargs: Any,
    ) -> None:
        if sample_rate is not None:
            self._sample_rate = sample_rate

        super()._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            z_score=z_score,
            **kwargs,
        )

    # Data Generation
    def generate_x(self, n_samples: int) -> Iterable:
        if self.x is not None:
            return np.squeeze(self.x)
        elif self._sample_rate is None:
            return tuple(range(0, n_samples))
        else:
            return np.arange(n_samples) / self._sample_rate

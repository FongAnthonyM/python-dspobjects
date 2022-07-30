""" thresholdperformanceplot.py

"""
# Package Header #
from ....header import *

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
from ....operations import iterdim
from ...bases import Figure, Subplot, BasePlot
from ..zeroonedomainplot import ZeroOneDomainPlot


# Definitions #
# Classes #
class ThresholdPerformancePlot(ZeroOneDomainPlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_hovertemplate: str | None = ("%{y:.4f} %{_y_unit}<br>" +
                                         "%{x:.4f} %{_x_unit}<br>" +
                                         "Threshold: %{text}")

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        thresholds: np.ndarray | None = None,
        labels: Iterable[str] | None = None,
        axis: int = 0,
        c_axis: int = 1,
        build: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self._thresholds: np.ndarray | None = None

        # Object Construction #
        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                x=x,
                y=y,
                thresholds=thresholds,
                labels=labels,
                axis=axis,
                c_axis=c_axis,
                build=build,
                **kwargs,
            )

    @property
    def thresholds(self) -> np.ndarray | None:
        return self._thresholds

    # Instance Methods #
    # Constructors/Destructors
    def _update_attributes(
        self,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        thresholds: np.ndarray | None = None,
        labels: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        **kwargs: Any,
    ) -> None:
        super()._update_attributes(
            x=x,
            y=y,
            labels=labels,
            axis=axis,
            c_axis=c_axis,
            **kwargs,
        )

        if thresholds is not None:
            if thresholds.shape != self.y.shape:
                raise ValueError("thresholds must be the same size as data")
            self._thresholds = thresholds

    def text_iterator(self, channels: int):
        if self._text is not None:
            if self.text.shape[self._c_axis] == 1:
                return itertools.repeat(np.squeeze(self._text), channels)
            else:
                return iterdim(self._text, self._c_axis)
        elif self._thresholds is not None:
            return (tuple(f"{v:.4f}" for v in c) for c in iterdim(self._thresholds, self._c_axis))
        elif self._z_score:
            return (tuple(f"{v:.4f}" for v in c) for c in iterdim(self.y, self._c_axis))
        else:
            return itertools.repeat(None, channels)

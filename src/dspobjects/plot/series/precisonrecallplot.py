""" precisonrecallplot.py

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

# Local Packages #
from .seriesplot import SeriesPlot


# Definitions #
# Classes #
class PresionRecallPlot(SeriesPlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(self, init: bool = True) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #


        # Object Construction #
        if init:
            self.construct()

    # Instance Methods #
    # Constructors/Destructors
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

        self.build_static_traces()

        if self.y is not None:
            self.update_plot()

    def build_static_traces(self) -> None:
        pass

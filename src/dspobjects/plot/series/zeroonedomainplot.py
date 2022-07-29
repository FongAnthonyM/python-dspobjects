""" zeroonedomainplot.py

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

# Local Packages #
from .seriesplot import SeriesPlot


# Definitions #
# Classes #
class ZeroOneDomainPlot(SeriesPlot):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_xaxis_settings: dict[str, Any] = dict(
        range=[0, 1],
        constrain="domain",
        scaleanchor="y",
        scaleratio=1,
        tickmode='linear',
        tick0=0,
        dtick=0.10,
        minor=dict(ticks="outside", nticks=10, showgrid=True),
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True
    )
    default_yaxis_settings: dict[str, Any] = dict(
        range=[0, 1],
        constrain="domain",
        scaleanchor="x",
        scaleratio=1,
        tickmode='linear',
        tick0=0,
        dtick=0.10,
        minor=dict(ticks="outside", nticks=10, showgrid=True),
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True
    )

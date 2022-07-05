""" iterdim.py
A function that iterates over a specfic dimension of an ndarray.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Standard Libraries #

# Third-Party Packages #
import numpy as np

# Local Packages #


# Definitions #
# Functions #
def iterdim(a: np.ndarray, axis: int = 0) -> np.ndarray:
    """Iterates over a given axis of an array.

    Args:
        a: The array to iterate through.
        axis: The axis to iterate over.

    Returns:
        The data at an element of the axis.
    """
    slices = (slice(None),) * axis
    for i in range(a.shape[axis]):
        yield a[slices + (i,)]

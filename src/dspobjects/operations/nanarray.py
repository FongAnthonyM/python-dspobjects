""" nanarray.py
A function that creates an array of NaNs.
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
from collections.abc import Iterable
from typing import Any

# Third-Party Packages #
import numpy as np

# Local Packages #


# Definitions #
def nan_array(shape: int | Iterable | tuple[int], dtype: object | None = None, **kwargs: Any) -> np.ndarray:
    """Creates an array of NaNs.

    Args:
        shape: The shape of the array to create.
        dtype: The data type of the array.
        **kwargs: The other numpy keyword arguments for creating an array.

    Returns:
        The array of NaNs.
    """
    a = np.empty(shape=shape, dtype=dtype, **kwargs)
    a.fill(np.nan)
    return a

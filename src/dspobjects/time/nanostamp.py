""" nanostamp.py
Create a nanostamp based on input
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
import datetime

# Third-Party Packages #
from baseobjects import singlekwargdispatch
import numpy as np

# Local Packages #
from .timestamp import Timestamp, NANO_SCALE


# Definitions #
# Functions #
@singlekwargdispatch("value")
def nanostamp(value: datetime.datetime | float | int | np.dtype, is_nano: bool = False) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        is_nano: Determines if the input is in nanoseconds.
    """
    raise TypeError(f"the start cannot be assigned to a {type(value)}")


@nanostamp.register
def _nanostamp(value: np.uint64, is_nano: bool = True) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        is_nano: Determines if the input is in nanoseconds.
    """
    if is_nano:
        return value
    else:
        return value * NANO_SCALE


@nanostamp.register
def _nanostamp(value: Timestamp, is_nano: bool = False) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        is_nano: Determines if the input is in nanoseconds.
    """
    return value.nanostamp()


@nanostamp.register
def _nanostamp(value: datetime.datetime, is_nano: bool = False) -> np.uint64:
    """Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        is_nano: Determines if the input is in nanoseconds.
    """
    return np.uint64(value.timestamp()) * NANO_SCALE


@nanostamp.register(float)
@nanostamp.register(int)
@nanostamp.register(np.dtype)
def _nanostamp(value: float | int | np.dtype, is_nano: bool = False) -> np.uint64:
    """"Creates a nanostamp from the input.

    Args:
        value: The value create the nanostamp from.
        is_nano: Determines if the input is in nanoseconds.
    """
    if is_nano:
        return np.uint64(value)
    else:
        return np.uint64(value) * NANO_SCALE

""" timestamp.py
Extends the pandas Timestamp class.
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
from datetime import timezone, tzinfo
from decimal import Decimal

# Third-Party Packages #
import numpy as np
import pandas as pd

# Local Packages #


# Definitions #
NANO_SCALE = np.uint64(10**9)


# Classes #
class Timestamp(pd.Timestamp):
    """Extends the pandas Timestamp class."""
    _UNIX_EPOCH = pd.Timestamp(1970, 1, 1)

    # Class Methods #
    @classmethod
    def fromnanostamp(cls, t: float | int | np.dtype, tz: tzinfo | None = timezone.utc) -> "Timestamp":
        return cls.fromtimestamp(t/10**9, tz)

    @classmethod
    def fromdecimal(cls, t: Decimal, tz: tzinfo | None = timezone.utc) -> "Timestamp":
        integer = np.uint64(round(t))
        nts = integer * _NANO_SCALE + np.uint64(t - integer) * _NANO_SCALE
        return cls._UNIX_EPOCH.replace(tzinfo=tz) + pd.Timedelta(nanoseconds=nts)

    # Instance Methods #
    def nanostamp(self) -> np.uint64:
        delta = self - self._UNIX_EPOCH
        return np.uint64(delta.total_seconds() * _NANO_SCALE) + np.uint64(delta.nanoseconds)

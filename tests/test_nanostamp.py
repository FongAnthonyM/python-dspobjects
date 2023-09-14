""" test_nan_array.py

"""
# Package Header #
from src.dspobjects.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import abc
import datetime
import pathlib

# Third-Party Packages #
import pytest
import numpy as np

# Local Packages #
from src.dspobjects.time import nanostamp, NANO_SCALE


# Definitions #
# Classes #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class ClassTest(abc.ABC):
    """Default class tests that all classes should pass."""

    class_ = None
    timeit_runs = 100000
    speed_tolerance = 200

    def test_instance_creation(self):
        pass


class TestNanostamp:
    def test_date(self):
        date = datetime.datetime.now(tz=datetime.timezone.utc).date()
        ns = nanostamp(date)
        assert (ns % 86400000000000) == 0

    def test_datetime(self):
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        ns = nanostamp(dt)
        assert ns == (dt.timestamp() * NANO_SCALE)

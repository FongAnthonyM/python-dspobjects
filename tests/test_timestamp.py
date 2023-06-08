""" test_timestamp.py

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
from src.dspobjects.time import Timestamp, nanostamp, get_localzone


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


class TestTimestamp:
    time_zones = (None, get_localzone(), datetime.timezone.utc)

    @pytest.mark.parametrize("tz", time_zones)
    def test_timestamp_nanostamp_accuracy(self, tz):
        ts = datetime.datetime.now(tz)
        ns = np.uint64(ts.timestamp() * 10**9)
        ts_other = datetime.datetime.fromtimestamp(ts.timestamp(), tz)
        ts_object = Timestamp.fromnanostamp(ns, tz)
        assert ts_object.timetuple() == ts_other.timetuple()

    @pytest.mark.parametrize("tz", time_zones)
    def test_timestamp_nanostamp_precision(self, tz):
        ts = datetime.datetime.now(tz).timestamp()
        ns = np.uint64(ts * 10**9) + np.uint64(111111111111111111)
        ts_object = Timestamp.fromnanostamp(ns, tz)
        new_ns = nanostamp(ts_object)
        assert new_ns == ns

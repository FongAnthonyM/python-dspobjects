""" test_plottimeseries.py

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
import pathlib

# Third-Party Packages #
import pytest
import numpy as np

# Local Packages #
from src.dspobjects.plot.plottimeseries import plot_time_series


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


class TestPlotTimeSeries():

    def generate_data(self, samples=1000, channels=128):
        voltages = np.random.rand(samples, channels) - .5
        return voltages

    def test_plot_time_series(self):
        data = self.generate_data()
        plot_time_series(y=data)



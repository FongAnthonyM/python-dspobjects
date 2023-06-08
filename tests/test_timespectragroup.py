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
from src.dspobjects.plot import Figure
from src.dspobjects.plot import TimeSpectraGroup


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


class TestTimeSpectraGroup:
    def generate_data(self, samples=10240, channels=10):
        voltages = np.random.rand(samples, channels) - 0.5
        return voltages

    def test_timeseriesplot_figure(self):
        data = self.generate_data()
        ts_group = TimeSpectraGroup()
        ts_group["timeseries"].build(y=data, sample_rate=1024.0)
        ts_group["spectra"].build(y=data)
        ts_group.figure.show()

    def test_timeseriesplot_subplot(self):
        data = self.generate_data()
        fig = Figure()
        fig.update_layout(title="Figure Name")
        fig.update_layout(TimeSeriesPlot.default_layout_settings)
        fig.set_subplots(1, 3, horizontal_spacing=0.05)
        plot1 = TimeSeriesPlot(subplot=fig.subplots[0][1], y=data, sample_rate=1024.0)
        plot2 = TimeSeriesPlot(subplot=fig.subplots[0][0], y=data, sample_rate=1024.0)
        plot1.update_title(text="Test Name")
        # plot2 = TimeSeriesPlot(subplot=fig.subplots[0][1], y=data, sample_rate=1024.0)
        fig.show()

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
from src.dspobjects.plot import BarPlot


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


class TestTimeSeriesPlot():

    def generate_data(self, samples=10, channels=1):
        counts = np.random.randint(1, 100, size=(samples, channels))
        return counts

    def test_vertical_plot(self):
        data = self.generate_data()
        fig = Figure()
        fig.set_subplots(1, 2)
        plot1 = BarPlot(subplot=fig.subplots[0][0], y=data, orientation='v')
        plot1.update_title(text="Test Name")
        fig.show()

    def test_horizontal_plot(self):
        data = self.generate_data()
        fig = Figure()
        fig.set_subplots(1, 2)
        plot1 = BarPlot(subplot=fig.subplots[0][0], x=data, orientation='h')
        plot1.update_title(text="Test Name")
        fig.show()

    def test_separated_vertical_plot(self):
        data = self.generate_data()
        fig = Figure()
        fig.set_subplots(1, 2)
        plot1 = BarPlot(subplot=fig.subplots[0][0], y=data, orientation='v', separated=True)
        plot1.update_title(text="Test Name")
        fig.show()

    def test_separated_horizontal_plot(self):
        data = self.generate_data()
        fig = Figure()
        fig.set_subplots(1, 2)
        plot1 = BarPlot(subplot=fig.subplots[0][0], x=data, orientation='h', separated=True)
        plot1.update_title(text="Test Name")
        fig.show()

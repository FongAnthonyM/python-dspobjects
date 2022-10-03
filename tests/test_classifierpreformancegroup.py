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
from src.dspobjects.plot import ClassifierPerformanceGroup


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


class TestClassifierPerformanceGroup():

    def generate_data(self, samples=10240, channels=10):
        # Create Signal
        rng = np.random.default_rng()
        amp = 1
        noise_power = 0.0001
        carrier = 1 - amp / np.log(np.arange(1, samples + 1) * np.e)
        carrier = np.flip(carrier)
        y = np.repeat(carrier[:, None], channels, axis=1)
        noise = rng.normal(scale=np.sqrt(noise_power), size=(samples, channels))
        y += noise

        x = np.linspace(0, 1, samples)
        return x, y

    def test_classifierperformancegroup_figure(self):
        x, y = self.generate_data()
        ts_group = ClassifierPerformanceGroup()
        ts_group["all"]["roc"].build(x=x, y=y)
        ts_group["all"]["precisionrecall"].build(x=x, y=y)
        ts_group["test"]["roc"].build(x=x, y=y)
        ts_group["test"]["precisionrecall"].build(x=x, y=y)
        ts_group.figure.show()

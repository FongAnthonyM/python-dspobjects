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
from scipy import signal

# Local Packages #
from src.dspobjects.plot import Figure
from src.dspobjects.plot import SpectrogramPlot


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


class TestSpectrogramsPlot:
    def generate_data(self, samples=10240, channels=10):
        # Create Signal
        rng = np.random.default_rng()
        fs = 10e3
        N = 1e5
        amp = 2 * np.sqrt(2)
        noise_power = 0.01 * fs / 2
        time = np.arange(N) / float(fs)
        mod = 500 * np.cos(2 * np.pi * 0.25 * time)
        carrier = amp * np.sin(2 * np.pi * 3e3 * time + mod)
        noise = rng.normal(scale=np.sqrt(noise_power), size=time.shape)
        noise *= np.exp(-time / 5)
        x = carrier + noise

        # Generate Spectrogram
        return signal.spectrogram(x, fs)

    def test_spectrogramplot_figure(self):
        f, t, Sxx = self.generate_data()
        plot1 = SpectrogramPlot(x=t, y=f, z=Sxx)
        plot1.update_title(text="Test Name")
        plot1._figure.write_html("test_spectrogram.html")
        plot1._figure.show(aspect="auto")

    def test_spectrogramplot_subplot(self):
        f, t, Sxx = self.generate_data()
        fig = Figure()
        fig.update_layout(title="Figure Name")
        fig.set_subplots(3, 1, horizontal_spacing=0.05)
        plot1 = SpectrogramPlot(subplot=fig.subplots[0][0], x=t, y=f, z=Sxx)
        # plot2 = SpectrogramPlot(subplot=fig.subplots[1][0], x=t, y=f, z=Sxx)
        plot1.update_title(text="Test Name")
        fig.show()

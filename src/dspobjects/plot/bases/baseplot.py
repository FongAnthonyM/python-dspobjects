""" baseplot.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from abc import abstractmethod
from collections.abc import Iterable, Iterator, Mapping
import itertools
from typing import Any

# Third-Party Packages #
from baseobjects import BaseObject, singlekwargdispatchmethod
import numpy as np
from plotly.basedatatypes import BaseTraceType
import plotly.graph_objects as go
import plotly.express as px

# Local Packages #
from .subplot import Subplot
from .figure import Figure


# Definitions #
# Classes #
class BasePlot(BaseObject):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_layout_settings: Mapping[str, Any] = dict(
        title=dict(
            font=dict(size=30),
            y=1.0,
            x=0.5,
            xanchor='center',
            yanchor='top'),
    )
    default_xaxis_settings: Mapping[str, Any] = dict()
    default_yaxis_settings: Mapping[str, Any] = dict()
    default_trace_settings: Mapping[str, Any] = dict()
    default_hovertemplate: str | None = None
    default_color_sequence: Iterable[str] | str | None = px.colors.qualitative.Plotly
    default_x_unit: str = ""
    default_y_unit: str = ""
    default_z_unit: str = ""

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        name: str = "",
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        z: np.ndarray | None = None,
        labels: list | None = None,
        label_index: bool = True,
        tick_index_only: bool = False,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 5.0,
        init: bool = True,
    ) -> None:
        # New Attributes #
        # Settings
        self._layout_settings: Mapping[str, Any] = self.default_layout_settings.copy()
        self._trace_settings_: Mapping[str, Any] = self.default_trace_settings.copy()
        self._hovertemplate_: str | None = self.default_hovertemplate

        self._color_squence: list | None = None
        self._color_cycle: Iterator | None = None

        self._name: str = ""
        self._trace_offset: float = 5.0

        self._axis: int = 0
        self._c_axis: int = 1

        self._label_index: bool = True
        self._tick_index_only: bool = True

        self._x_unit: str = self.default_x_unit
        self._y_unit: str = self.default_y_unit
        self._z_unit: str = self.default_z_unit

        # Component Objects
        self._figure: go.Figure | None = None
        self._subplot: Subplot | None = None
        self._xaxis: go.layout.XAxis | None = None
        self._yaxis: go.layout.YAxis | None = None

        # Data
        self._x = None
        self._y = None
        self._z = None

        self._labels = None

        self._traces: list = []

        # Object Construction #
        if self.default_color_sequence is not None:
            self._color_squence = self.default_color_sequence.copy()
            self._color_cycle = itertools.cycle(self._color_squence)

        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                name=name,
                x=x,
                y=y,
                z=z,
                labels=labels,
                label_index=label_index,
                tick_index_only=tick_index_only,
                axis=axis,
                c_axis=c_axis,
                t_offset=t_offset,
            )

    @property
    def _trace_settings(self) -> Mapping[str, Any]:
        _trace_settings = self._trace_settings_.copy()
        if "hovertemplate" not in _trace_settings and self._hovertemplate:
            _trace_settings["hovertemplate"] = self._hovertemplate

        return _trace_settings

    @_trace_settings.setter
    def _trace_settings(self, value: Mapping[str, Any]) -> None:
        self._trace_settings_ = value

    @property
    def _hovertemplate(self) -> str:
        if self._hovertemplate_ is not None:
            _hovertemplate = self._hovertemplate_.replace("%{_x_unit}", self._x_unit)
            _hovertemplate = _hovertemplate.replace("%{_y_unit}", self._y_unit)
            _hovertemplate = _hovertemplate.replace("%{_z_unit}", self._z_unit)
            return _hovertemplate
        else:
            return None

    @_hovertemplate.setter
    def _hovertemplate(self, value: str) -> None:
        self._hovertemplate_ = value

    @property
    def trace_offset(self) -> float:
        return self._trace_offset

    @property
    def axis(self) -> int:
        return self._axis

    @property
    def c_axis(self) -> int:
        return self._c_axis

    @property
    def label_index(self) -> bool:
        return self._label_index

    # Todo: Add these
    self._tick_index_only: bool = True

    self._x_unit: str = self.default_x_unit
    self._y_unit: str = self.default_y_unit
    self._z_unit: str = self.default_z_unit

    @property
    def figure(self) -> go.Figure | None:
        return self._figure

    @property
    def subplot(self) -> Subplot | None:
        return self._subplot

    @property
    def xaxis(self) -> go.layout.XAxis | None:
        if self._xaxis is not None:
            return self._xaxis
        elif self._subplot is not None:
            return self._subplot.xaxis
        elif self._figure is not None:
            return self._figure.layout.xaxis
        else:
            return None

    @property
    def yaxis(self) -> go.layout.YAxis | None:
        if self._yaxis is not None:
            return self._yaxis
        elif self._subplot is not None:
            return self._subplot.yaxis
        elif self._figure is not None:
            return self._figure.layout.yaxis
        else:
            return None

    @property
    def x(self) -> np.ndarray | None:
        return self._x

    @x.setter
    def x(self, value) -> None:
        if value is None:
            self._x = None
        else:
            value = value if isinstance(value, np.ndarray) else np.array(value)
            value = value if value.ndim > 1 else np.expand_dims(value, 1)
            self._x = value

    @property
    def y(self) -> np.ndarray | None:
        return self._y

    @y.setter
    def y(self, value) -> None:
        if value is None:
            self._y = None
        else:
            value = value if isinstance(value, np.ndarray) else np.array(value)
            value = value if value.ndim > 1 else np.expand_dims(value, 1)
            self._y = value

    @property
    def z(self) -> np.ndarray | None:
        return self._z

    @z.setter
    def z(self, value) -> None:
        if value is None:
            self._z = None
        else:
            value = value if isinstance(value, np.ndarray) else np.array(value)
            value = value if value.ndim > 1 else np.expand_dims(value, 1)
            self._z = value

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        name: str | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        z: np.ndarray | None = None,
        labels: list | None = None,
        label_index: bool | None = None,
        tick_index_only: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
    ) -> None:
        if figure is not None and subplot is not None:
            if  subplot.figure != figure:
                raise ValueError("The _figure and _subplot do match.")

        if figure is not None:
            self._figure = figure
            self._figure.update_layout(self.default_layout_settings)
        elif self._figure is None and subplot is None:
            self._figure = Figure()
            self._figure.update_layout(self.default_layout_settings)

        if subplot is not None:
            self._subplot = subplot
            self._figure = subplot.figure

        if name is not None:
            self._name = name

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if z is not None:
            self.z = z

        if labels is not None:
            self._labels = labels

        if label_index is not None:
            self._label_index = label_index

        if tick_index_only is not None:
            self._tick_index_only = tick_index_only

        if axis is not None:
            self._axis = axis

        if c_axis is not None:
            self._c_axis = c_axis

        if t_offset is not None:
            self._trace_offset = t_offset

        self.update_xaxis(self.default_xaxis_settings)
        self.update_yaxis(self.default_yaxis_settings)

    def _update_attributes(
        self,
        figure: go.Figure | None = None,
        subplot: Subplot | None = None,
        name: str | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        z: np.ndarray | None = None,
        labels: list | None = None,
        label_index: bool | None = None,
        tick_index_only: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
    ) -> None:
        if figure is not None and subplot is not None:
            if subplot.figure != figure:
                raise ValueError("The _figure and _subplot do match.")

        if figure is not None:
            self._figure = figure
            self._figure.update_layout(self.default_layout_settings)
        elif self._figure is None and subplot is None:
            self._figure = Figure()
            self._figure.update_layout(self.default_layout_settings)

        if subplot is not None:
            self._subplot = subplot
            self._figure = subplot.figure

        if name is not None:
            self._name = name

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if z is not None:
            self.z = z

        if labels is not None:
            self._labels = labels

        if label_index is not None:
            self._label_index = label_index

        if tick_index_only is not None:
            self._tick_index_only = tick_index_only

        if axis is not None:
            self._axis = axis

        if c_axis is not None:
            self._c_axis = c_axis

        if t_offset is not None:
            self._trace_offset = t_offset

    # Subplot and Axes
    def set_subplot(self, subplot: Subplot) -> None:
        if subplot.figure != self._figure:
            raise ValueError("Cannot change plot to different _figure, create new plot instead.")

        self._subplot = subplot

        for trace in self._traces:
            x_subplot = f"x{'' if (subplot.row - 1) <= 0 else (subplot.row - 1)}"
            y_subplot = f"y{'' if (subplot.col - 1) <= 0 else (subplot.col - 1)}"
            trace.update(xaxis=x_subplot, yaxis=y_subplot)

    def set_xaxis(self, xaxis: go.layout.XAxis) -> None:
        self._xaxis = xaxis
        axis_name = xaxis.plotly_name.replace("_axis", '')
        for trace in self._traces:
            trace.update(xaxis=axis_name)

    def set_yaxis(self, yaxis: go.layout.YAxis) -> None:
        self._yaxis = yaxis
        axis_name = yaxis.plotly_name.replace("_axis", '')
        for trace in self._traces:
            trace.update(yaxis=axis_name)

    def update_title(self, dict1: Mapping[str, Any] = None, overwrite: bool =False, **kwargs: Any) -> None:
        if self._subplot is not None:
            self._subplot.title.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self._figure.layout.title.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def update_xaxis(self, dict1: Mapping[str, Any] = None, overwrite: bool =False, **kwargs: Any) -> None:
        if self._subplot is not None:
            self._subplot.xaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self._figure.layout.xaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def update_yaxis(self, dict1: Mapping[str, Any] = None, overwrite: bool =False, **kwargs: Any) -> None:
        if self._subplot is not None:
            self._subplot.yaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self._figure.layout.yaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)

    # Traces
    @abstractmethod
    def set_trace_color(self, trace: int | BaseTraceType, color: str) -> None:
        if isinstance(trace, int):
            trace = self._traces[trace]

    def _add_traces(self, traces: Iterable[BaseTraceType]) -> None:
        trace_defaults = dict()
        if self._xaxis is not None:
            updates["xaxis"] = self._xaxis.plotly_name.replace("_axis", '')

        if self._yaxis is not None:
            updates["yaxis"] = self._yaxis.plotly_name.replace("_axis", '')

        for trace in traces:
            if self._subplot is not None:
                new_trace = self._subplot.add_trace(trace)
            else:
                self._figure.add_trace(trace)
                new_trace = self._figure.data[-1]

            new_trace.update(trace_defaults)

            if self._color_squence is not None:
                self.set_trace_color(new_trace, next(self._color_cycle))

            self._traces.append(new_trace)

    @singlekwargdispatchmethod("_traces")
    def add_traces(self, traces, *args: BaseTraceType) -> None:
        raise ValueError(f"{type(traces)} is an invalid type for add_trace")

    @add_traces.register
    def _add_traces_(self, traces: BaseTraceType, *args: BaseTraceType) -> None:
        self._add_traces(traces=itertools.chain((traces,), args))

    @add_traces.register(Iterable)
    def _add_traces_(self, traces: Iterable[BaseTraceType], *args: BaseTraceType) -> None:
        self._add_traces(traces=itertools.chain(traces, args))

    def update_traces(self, dict1: Mapping[str, Any] = None, overwrite: bool =False, **kwargs: Any) -> None:
        for trace in self._traces:
            trace.update(dict1=dict1, overwrite=overwrite, **kwargs)

    # Trace/Legend
    @singlekwargdispatchmethod("plots")
    def group_same_legend_items(self, plots: "BasePlot", *args: "BasePlot") -> None:
        if not isinstance(plots, BasePlot):
            raise ValueError(f"{type(plots)} is an invalid type for group_same_legend")

        for trace in self._traces:
            trace.legendgroup = trace.name

        for plot in itertools.chain((plots,), args):
            for trace in plot._traces:
                trace.legendgroup = trace.name
                trace.showlegend = False

    @group_same_legend_items.register(Iterable)
    def _group_same_legend_items(self, plots: Iterable["BasePlot"], *args: "BasePlot") -> None:
        for trace in self._traces:
            trace.legendgroup = trace.name

        for plot in itertools.chain(plots, args):
            for trace in plot._traces:
                trace.legendgroup = trace.name
                trace.showlegend = False

    # Data Generation
    def generate_x(self, n_samples: int) -> tuple | np.ndarray:
        return tuple(range(n_samples))

    def generate_y(self, n_samples: int) -> tuple | np.ndarray:
        return tuple(range(n_samples))

    def generate_z(self, n_samples: int) -> tuple | np.ndarray:
        return tuple(range(0, n_samples))
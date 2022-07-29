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
import copy
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
from .tracecontainer import TraceContainer
from .figure import Figure


# Definitions #
# Classes #
class BasePlot(BaseObject):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    default_layout_settings: dict[str, Any] = dict(
        title=dict(
            font=dict(size=30),
            y=1.0,
            x=0.5,
            xanchor='center',
            yanchor='top'),
    )
    default_title_settings: dict[str, Any] = dict()
    default_xaxis_settings: dict[str, Any] = dict()
    default_yaxis_settings: dict[str, Any] = dict()
    default_static_trace_settings: dict[str, Any] = dict(showlegend=False)
    default_trace_settings: dict[str, Any] = dict()
    default_hovertemplate: str | None = None
    default_color_sequence: Iterable[str] | str | None = px.colors.qualitative.Plotly
    default_x_unit: str = ""
    default_y_unit: str = ""
    default_z_unit: str = ""
    default_static_traces: dict[str, BaseTraceType] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        name: str = "",
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        z: np.ndarray | None = None,
        text: Iterable[str] | None = None,
        labels: list | None = None,
        label_axis: bool = False,
        label_index: bool = True,
        tick_index_only: bool = False,
        names: list | None = None,
        axis: int = 0,
        c_axis: int = 1,
        t_offset: float = 5.0,
        trace_settings: dict[str, Any] | None = None,
        title: dict[str, Any] | None = None,
        xaxis: dict[str, Any] | None = None,
        yaxis: dict[str, Any] | None = None,
        static_traces: dict[str, BaseTraceType] | None = None,
        static_trace_settings: dict[str, Any] | None = None,
        build: bool = True,
        init: bool = True,
    ) -> None:
        # New Attributes #
        # Settings
        self._layout_settings: dict[str, Any] = self.default_layout_settings.copy()
        self._trace_settings_: dict[str, Any] = self.default_trace_settings.copy()
        self._hovertemplate_: str | None = self.default_hovertemplate
        self._static_trace_settings: dict[str, Any] = self.default_static_trace_settings.copy()
        self._static_traces: dict[str, BaseTraceType] = self.default_static_traces.copy()
        self._group_existing_legend: bool = False

        self._color_sequence: list | None = None
        self._color_cycle: Iterator | None = None

        self._name: str = ""
        self._names: Iterable[str] | None = None
        self._trace_offset: float = 5.0

        self._axis: int = 0
        self._c_axis: int = 1

        self._label_axis: bool = True
        self._label_index: bool = True
        self._tick_index_only: bool = True

        self._x_unit: str = self.default_x_unit
        self._y_unit: str = self.default_y_unit
        self._z_unit: str = self.default_z_unit

        # Component Objects
        self._figure: Figure | None = None
        self._subplot: Subplot | None = None
        self._xaxis: go.layout.XAxis | None = None
        self._yaxis: go.layout.YAxis | None = None

        # Data
        self._x: np.ndarray | None = None
        self._y: np.ndarray | None = None
        self._z: np.ndarray | None = None
        self._text: np.ndarray | None = None

        self._labels: Iterable[str] | None = None

        self._traces: TraceContainer | None = None

        # Object Construction #
        if self.default_color_sequence is not None:
            self._color_sequence = copy.copy(self.default_color_sequence)
            self._color_cycle = itertools.cycle(self._color_sequence)

        if init:
            self.construct(
                figure=figure,
                subplot=subplot,
                name=name,
                x=x,
                y=y,
                z=z,
                text=text,
                labels=labels,
                label_axis=label_axis,
                label_index=label_index,
                tick_index_only=tick_index_only,
                names=names,
                axis=axis,
                c_axis=c_axis,
                t_offset=t_offset,
                trace_settings=trace_settings,
                title=title,
                xaxis=xaxis,
                yaxis=yaxis,
                static_traces=static_traces,
                static_trace_settings=static_trace_settings,
                build=build,
            )

    @property
    def _trace_settings(self) -> dict[str, Any]:
        _trace_settings = self._trace_settings_.copy()
        if "hovertemplate" not in _trace_settings and self._hovertemplate:
            _trace_settings["hovertemplate"] = self._hovertemplate

        return _trace_settings

    @_trace_settings.setter
    def _trace_settings(self, value: Mapping[str, Any]) -> None:
        self._trace_settings_ = value

    @property
    def _hovertemplate(self) -> str | None:
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
    def color_sequence(self) -> Iterable[str] | None:
        return self._color_sequence

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

    @property
    def tick_index_only(self) -> bool:
        return self._tick_index_only

    @property
    def x_unit(self) -> str:
        return self._x_unit

    @property
    def y_unit(self) -> str:
        return self._y_unit

    @property
    def z_unit(self) -> str:
        return self._z_unit

    @property
    def figure(self) -> Figure | None:
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

    @property
    def text(self) -> np.ndarray | None:
        return self._text

    @text.setter
    def text(self, value) -> None:
        if value is None:
            self._text = None
        else:
            value = value if isinstance(value, np.ndarray) else np.array(value)
            value = value if value.ndim > 1 else np.expand_dims(value, 1)
            self._text = value

    @property
    def labels(self) -> Iterable[str]:
        return copy.copy(self._labels)

    @property
    def names(self) -> Iterable[str]:
        return self._names

    @property
    def trace_groups(self) -> dict[str, Iterable[BaseTraceType]]:
        return self._trace_groups

    @property
    def traces(self) -> tuple[BaseTraceType]:
        return tuple(self._traces)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        name: str | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        z: np.ndarray | None = None,
        text: Iterable[str] | None = None,
        labels: list | None = None,
        label_axis: bool | None = None,
        label_index: bool | None = None,
        tick_index_only: bool | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        trace_settings: dict[str, Any] | None = None,
        title: dict[str, Any] | None = None,
        xaxis: dict[str, Any] | None = None,
        yaxis: dict[str, Any] | None = None,
        static_traces: dict[str, BaseTraceType] | None = None,
        static_trace_settings: dict[str, Any] | None = None,
        build: bool = True,
        **kwargs: Any,
    ) -> None:
        self._update_attributes(
            figure=figure,
            subplot=subplot,
            name=name,
            x=x,
            y=y,
            z=z,
            text=text,
            labels=labels,
            label_axis=label_axis,
            label_index=label_index,
            tick_index_only=tick_index_only,
            axis=axis,
            c_axis=c_axis,
            t_offset=t_offset,
            trace_settings=trace_settings,
            static_traces=static_traces,
            static_trace_settings=static_trace_settings,
            **kwargs,
        )

        title_settings = self.default_title_settings | title if title is not None else self.default_title_settings
        xaxis_settings = self.default_xaxis_settings | xaxis if xaxis is not None else self.default_xaxis_settings
        yaxis_settings = self.default_yaxis_settings | yaxis if yaxis is not None else self.default_yaxis_settings

        self.update_title(title_settings)
        self.update_xaxis(xaxis_settings)
        self.update_yaxis(yaxis_settings)

        if build:
            self.build()

    def _update_attributes(
        self,
        figure: Figure | None = None,
        subplot: Subplot | None = None,
        name: str | None = None,
        x: np.ndarray | None = None,
        y: np.ndarray | None = None,
        z: np.ndarray | None = None,
        text: Iterable[str] | None = None,
        labels: list | None = None,
        label_axis: bool | None = None,
        label_index: bool | None = None,
        tick_index_only: bool | None = None,
        names: list | None = None,
        axis: int | None = None,
        c_axis: int | None = None,
        t_offset: float | None = None,
        trace_settings: dict[str, Any] | None = None,
        static_traces: dict[str, BaseTraceType] | None = None,
        static_trace_settings: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        if figure is not None and subplot is not None:
            if subplot.figure != figure:
                raise ValueError("The _figure and _subplot do match.")

        if figure is not None:
            self._figure = figure
        elif self._figure is None and subplot is None:
            self._figure = Figure()
            self._figure.update_layout(self.default_layout_settings)

        if subplot is not None:
            self._subplot = subplot
            self._figure = subplot.figure

        if self._traces is None:
            self._traces = self._figure.create_trace_group(str(id(self)))
            self._traces.require_group("static")
            self._traces.require_group("data")

        if name is not None:
            self._name = name

        if names is not None:
            self._names = names

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if z is not None:
            self.z = z

        if text is not None:
            self.text = text

        if labels is not None:
            self._labels = labels

        if label_axis is not None:
            self._label_axis = label_axis

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

        if trace_settings is not None:
            self._trace_settings_.update(trace_settings)

        if static_traces is not None:
            self._static_traces.update(static_traces)

        if static_trace_settings is not None:
            self._static_trace_settings.update(static_trace_settings)

    def build(self, *args: Any, **kwargs: Any) -> None:
        self._update_attributes(*args, **kwargs,)
        self.build_static_traces()

    def build_static_traces(self, static_traces: dict[str, BaseTraceType] | None = None, **kwargs: Any) -> None:
        if static_traces is not None:
            self._static_traces.update(static_traces)
        self.add_static_traces(self._static_traces)

    # Subplot and Axes
    def _set_subplot(self, row: int, col: int):
        for trace in self._traces:
            x_subplot = f"x{'' if (row - 1) <= 0 else (row - 1)}"
            y_subplot = f"y{'' if (col - 1) <= 0 else (col - 1)}"
            trace.update(xaxis=x_subplot, yaxis=y_subplot)

    @singlekwargdispatchmethod
    def set_subplot(self, subplot: Subplot | None = None, row: int | None = None, col: int | None = None):
        raise ValueError(f"{type(subplot)} is an invalid type for set_subplot")

    @set_subplot.register
    def _set_subplot_(self, subplot: Subplot, **kwargs: Any):
        if subplot.figure != self._figure:
            raise ValueError("Cannot change plot to different figure, create new plot instead.")

        self._subplot = subplot
        self._set_subplot(row=subplot.row, col=subplot.col)

    @set_subplot.register
    def _set_subplot_(self, row: int, col: int, **kwargs: Any):
        self._subplot = self._figure.get_subplot(row=row, col=col)
        self._set_subplot(row=row, col=col)

    def set_xaxis(self, xaxis: go.layout.XAxis) -> None:
        self._xaxis = xaxis
        axis_name = xaxis.plotly_name.replace("axis", '')
        for trace in self._traces:
            trace.update(xaxis=axis_name)

    def set_yaxis(self, yaxis: go.layout.YAxis) -> None:
        self._yaxis = yaxis
        axis_name = yaxis.plotly_name.replace("axis", '')
        for trace in self._traces:
            trace.update(yaxis=axis_name)

    def update_title(self, dict1: dict[str, Any] = None, overwrite: bool = False, **kwargs: Any) -> None:
        if self._subplot is not None:
            self._subplot.title.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self._figure.layout.title.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def update_xaxis(self, dict1: dict[str, Any] = None, overwrite: bool = False, **kwargs: Any) -> None:
        if self._subplot is not None:
            self._subplot.xaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self._figure.layout.xaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)

    def update_yaxis(self, dict1: dict[str, Any] = None, overwrite: bool = False, **kwargs: Any) -> None:
        if self._subplot is not None:
            self._subplot.yaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)
        else:
            self._figure.layout.yaxis.update(dict1=dict1, overwrite=overwrite, **kwargs)

    # TraceContainer
    @abstractmethod
    def set_trace_color(self, trace: int | BaseTraceType, color: str) -> None:
        if isinstance(trace, int):
            trace = self._traces[trace]

    def _add_traces(self, traces: Iterable[BaseTraceType], group: str | Iterable[str] | None = None) -> None:
        if group is not None:
            contained_traces = self._traces.require_group(group)
        else:
            contained_traces = self._traces

        # Trace Settings
        trace_defaults = self._trace_settings.copy()
        if self._xaxis is not None:
            trace_defaults["xaxis"] = self._xaxis.plotly_name.replace("axis", '')

        if self._yaxis is not None:
            trace_defaults["yaxis"] = self._yaxis.plotly_name.replace("axis", '')

        for trace in traces:
            if self._subplot is not None:
                new_trace = self._subplot.add_trace(trace, traces=contained_traces)
            else:
                new_trace = contained_traces.append_trace(trace)

            new_trace.update(trace_defaults)

            if self._color_sequence is not None:
                self.set_trace_color(new_trace, next(self._color_cycle))

    @singlekwargdispatchmethod("traces")
    def add_traces(self, traces, *args: BaseTraceType, group: str | Iterable[str] | None = None) -> None:
        raise ValueError(f"{type(traces)} is an invalid type for add_trace")

    @add_traces.register
    def _add_traces_(
        self,
        traces: BaseTraceType,
        *args: BaseTraceType,
        group: str | Iterable[str] | None = None,
    ) -> None:
        self._add_traces(traces=itertools.chain((traces,), args), group=group)

    @add_traces.register(Iterable)
    def _add_traces_(
        self,
        traces: Iterable[BaseTraceType],
        *args: BaseTraceType,
        group: str | Iterable[str] | None = None,
    ) -> None:
        self._add_traces(traces=itertools.chain(traces, args), group=group)

    def update_traces(
        self,
        dict1: dict[str, Any] = None,
        overwrite: bool = False,
        trace_group: str | Iterable[str] | None = None,
        **kwargs: Any,
    ) -> None:
        traces = self._traces if trace_group is None else self._traces.get_group(trace_group)
        for trace in traces:
            trace.update(dict1=dict1, overwrite=overwrite, **kwargs)

    # Trace/Legend
    @singlekwargdispatchmethod("plots")
    def group_same_legend_items(self, plots: "BasePlot", *args: "BasePlot") -> None:
        if not isinstance(plots, BasePlot):
            raise ValueError(f"{type(plots)} is an invalid type for group_same_legend")

        self._group_existing_legend = True
        for trace in self._traces:
            trace.legendgroup = trace.name

        for plot in itertools.chain((plots,), args):
            plot._group_existing_legend = True
            for trace in plot._traces:
                trace.legendgroup = trace.name
                trace.showlegend = False

    @group_same_legend_items.register(Iterable)
    def _group_same_legend_items(self, plots: Iterable["BasePlot"], *args: "BasePlot") -> None:
        self._group_existing_legend = True
        for trace in self._traces:
            trace.legendgroup = trace.name

        for plot in itertools.chain(plots, args):
            plot._group_existing_legend = True
            for trace in plot._traces:
                trace.legendgroup = trace.name
                trace.showlegend = False

    # Data Generation
    def generate_x(self, n_samples: int) -> tuple | np.ndarray:
        return tuple(range(n_samples)) if self.x is None else np.squeeze(self.x)

    def generate_y(self, n_samples: int) -> tuple | np.ndarray:
        return tuple(range(n_samples)) if self.y is None else np.squeeze(self.y)

    def generate_z(self, n_samples: int) -> tuple | np.ndarray:
        return tuple(range(0, n_samples))

    def generate_labels(self, n_labels: int) -> Iterable[str]:
        if self._labels is None:
            return [f"Channel {i}" for i in range(1, n_labels + 1)]
        elif self._label_index:
            return [f"[Index {i + 1}] {label}" for i, label in enumerate(self._labels)]
        else:
            return self._labels

    def generate_names(self, names: Iterable[str] | None = None, n_names: int | None = None) -> list[str]:
        if self._names is not None:
            return [f"[Index {i + 1}] {name}" for i, name in enumerate(names)] if self._label_index else self._names
        elif names is not None:
            return [f"[Set {i + 1}] {name}" for i, name in enumerate(names)] if self._label_index else names
        elif self._label_index:
            return [f"[Set {i + 1}] Bar Set {i + 1}" for i in range(n_names)]
        else:
            return [f"Set {i + 1}" for i in range(n_names)]

    def generate_tick_labels(self, labels: Iterable[str]) -> list[str]:
        # Apply Index to Labels
        if self._label_index:
            if self._tick_index_only:
                tick_labels = [f"[Index {i + 1}]" for i, name in enumerate(labels)]
            else:
                tick_labels = [f"{name} [Index {i + 1}]" for i, name in enumerate(labels)]
        else:
            tick_labels = labels

        return tick_labels

    # Plotting
    def add_static_trace(self, name: str, trace: BaseTraceType) -> None:
        # Trace Settings
        trace_defaults = self._static_trace_settings.copy()
        if self._xaxis is not None:
            trace_defaults["xaxis"] = self._xaxis.plotly_name.replace("axis", '')

        if self._yaxis is not None:
            trace_defaults["yaxis"] = self._yaxis.plotly_name.replace("axis", '')

        trace_group = self._traces["static"].create_group(name)
        if self._subplot is not None:
            new_trace = self._subplot.add_trace(trace, traces=trace_group)
        else:
            new_trace = trace_group.append_trace(trace)
        new_trace.update(trace_defaults)

    def add_static_traces(self, dict_: dict[str, BaseTraceType]) -> None:
        # Trace Settings
        trace_defaults = self._static_trace_settings.copy()
        if self._xaxis is not None:
            trace_defaults["xaxis"] = self._xaxis.plotly_name.replace("axis", '')

        if self._yaxis is not None:
            trace_defaults["yaxis"] = self._yaxis.plotly_name.replace("axis", '')

        for name, trace in dict_.items():
            trace_group = self._traces["static"].create_group(name)
            if self._subplot is not None:
                new_trace = self._subplot.add_trace(trace, traces=trace_group)
            else:
                new_trace = trace_group.append_trace(trace)
            new_trace.update(trace_defaults)

    def update_static_trace(self, name: str, dict_: dict[str, Any]) -> None:
        self._traces["static"][name][0].update(dict_)

    def update_static_traces(self, dict_: dict[str, dict] | None) -> None:
        for name, updates in dict_.items():
            self._traces["static"][name][0].update(updates)

    def update_plot(self, **kwargs):
        pass

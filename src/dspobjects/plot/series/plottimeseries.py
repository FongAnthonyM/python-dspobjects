""" plottimeseries.py

"""
# Package Header #
from dspobjects.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Local Packages #
from dspobjects.operations import iterdim


# Definitions #


def plot_time_series(fig=None, x=None, y=None, sample_rate=None, labels=None, axis=0, c_axis=1, zscore=True, scale=10):
    fig = fig or go.Figure()
    fig.set_subplots(2,2)

    if zscore:
        y_mod = (y - np.nanmean(y, axis=axis)) / np.nanstd(y, axis=axis)
    else:
        y_mod = y

    n_channels = int(y.shape[c_axis])
    if labels is None:
        labels = [f"Channel {i}" for i in range(1, n_channels + 1)]

    x_title = ""
    if x is None:
        if len(y.shape) == 1:
            n_samples = y.shape[0]
        else:
            n_samples = y.shape[axis]

        if sample_rate is None:
            x = tuple(range(0, n_samples))
            x_title = "Samples"
        else:
            x = np.arange(0, n_samples) / sample_rate
            x_title = "Seconds"

    # Add traces
    traces = []
    layout_kwargs = {}
    for i, (plot_c, channel) in enumerate(zip(iterdim(y_mod, c_axis), iterdim(y, c_axis))):
        trace = go.Scattergl(
            x=x,
            y=plot_c + (i * scale),
            name=labels[i],
            text=[f"{c:.4f}" for c in channel],
        )
        traces.append(trace)
        fig.add_trace(trace,1,1)


    # style all the traces
    fig.update_traces(
        hovertemplate=
            '%{text} mV<br>' +
            '%{x} s',
        line={"width": 1},
        mode='lines',
        showlegend=True
    )

    # Update axes
    fig.update_layout(
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            title=dict(
                text=x_title,
                font=dict(
                    size=18
                ),
            ),
            autorange=True,
            fixedrange=True,
            range=[x[0], x[-1]],
            rangeslider=dict(
                autorange=False,
                range=[x[0], x[-1]],
                yaxis=dict(rangemode="auto")
            ),
        ),
    )

    # fig.update_layout(**layout_kwargs)
    fig.update_layout(yaxis=dict(
        anchor="free",
        autorange=False,
        mirror=True,
        showline=True,
        side="left",
        tickmode="auto",
        ticks="",
        type="linear",
        zeroline=False,
    ))



    # Update new_layout_settings
    fig.update_yaxes(
        range=[-1*scale, n_channels*scale],
        showgrid=False,
        tickmode="array",
        tickvals=np.arange(n_channels) * scale,
        ticktext=labels,
    )

    fig.update_layout(
        dragmode="zoom",
        # hovermode="x",
        legend=dict(traceorder="reversed"),
        template="plotly_white",
        # height=6000,
        margin=dict(
            t=50,
            b=50
        ),
        modebar_add=['drawline',
                     'drawopenpath',
                     'drawclosedpath',
                     'drawcircle',
                     'drawrect',
                     'eraseshape'
                     ],
    )

    return fig


def plot_spectra_series(fig=None, x=None, y=None, labels=None, axis=0, c_axis=1, zscore=True, scale=7):
    fig = fig or go.Figure()

    if zscore:
        y_mod = (y - np.nanmean(y, axis=axis)) / np.nanstd(y, axis=axis)
    else:
        y_mod = y

    n_channels = int(y.shape[c_axis])
    if labels is None:
        labels = [f"Channel {i}" for i in range(1, n_channels + 1)]

    x_title = "HZ"
    if x is None:
        if len(y.shape) == 1:
            n_samples = y.shape[0]
        else:
            n_samples = y.shape[axis]

    # Add traces
    layout_kwargs = {}
    for i, (plot_c, channel) in enumerate(zip(iterdim(y_mod, c_axis), iterdim(y, c_axis))):
        fig.add_trace(go.Scattergl(
            x=x,
            y=plot_c+(i*scale),
            name=labels[i],
            text=[f"{c:.4f}" for c in channel],
        ))


    # style all the traces
    fig.update_traces(
        hovertemplate=
            '%{text}<br>' +
            '%{x} Hz',
        line={"width": 1},
        mode='lines',
        showlegend=True
    )

    # Update axes
    fig.update_layout(
        xaxis=dict(
            showspikes=True,
            spikemode="across",
            title=dict(
                text=x_title,
                font=dict(
                    size=18
                ),
            ),
            autorange=True,
            fixedrange=True,
            range=[x[0], x[-1]],
            rangeslider=dict(
                autorange=False,
                range=[x[0], x[-1]],
                yaxis=dict(rangemode="auto")
            ),
        ),
    )

    # fig.update_layout(**layout_kwargs)
    fig.update_layout(yaxis=dict(
        anchor="free",
        autorange=False,
        mirror=True,
        showline=True,
        side="left",
        tickmode="auto",
        ticks="",
        type="linear",
        zeroline=False,
    ))

    # Update new_layout_settings
    fig.update_yaxes(
        range=[-1*scale, n_channels*scale],
        showgrid=False,
        tickmode="array",
        tickvals=np.arange(n_channels) * scale,
        ticktext=labels,
    )

    fig.update_layout(
        dragmode="zoom",
        # hovermode="x",
        legend=dict(traceorder="reversed"),
        template="plotly_white",
        # height=6000,
        margin=dict(
            t=50,
            b=50
        ),
        modebar_add=['drawline',
                     'drawopenpath',
                     'drawclosedpath',
                     'drawcircle',
                     'drawrect',
                     'eraseshape'
                     ],
    )

    return fig

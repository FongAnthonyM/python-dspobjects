""" plottimeseries.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #
import plotly.graph_objects as go
import plotly.express as px

# Local Packages #
from ..operations import iterdim


# Definitions #
def plot_time_series(fig=None, x=None, y=None, axis=0, c_axis=1):
    fig = fig or go.Figure()

    if x is None:
        if len(y.shape) == 1:
            n_samples = y.shape[0]
        else:
            n_samples = y.shape[axis]

        x = tuple(range(0, n_samples))

    n_channels = y.shape[c_axis]

    # Add traces
    layout_kwargs = {}
    for i, channel in enumerate(iterdim(y, c_axis)):
        fig.add_trace(go.Scatter(
            x=x,
            y=channel+i,
            name=f"Channel {i}",
            text=[f"{x:.4f}" for x in channel],
            )
        )


    # style all the traces
    fig.update_traces(
        hoverinfo="name+x+text",
        line={"width": 1},
        mode='lines',
        showlegend=True
    )

    # Update axes
    fig.update_layout(
        xaxis=dict(
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
        autorange=True,
        mirror=True,
        showline=True,
        side="left",
        tickmode="auto",
        ticks="",
        type="linear",
        zeroline=False,
    ))



    # Update layout
    fig.update_yaxes(showgrid=False)
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
    )

    fig.show()



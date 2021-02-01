# Copyright 2020 OpenRCA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import math
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sb

from orca_tools.common import logger, utils

LOG = logger.get_logger(__name__)


class PlotHelperMixin:

    def _set_font_size(self, size):
        plt.rc("font", size=size)
        plt.rc("axes", titlesize=size + 2)
        plt.rc("axes", labelsize=size)
        plt.rc("xtick", labelsize=size)
        plt.rc("ytick", labelsize=size)
        plt.rc("legend", fontsize=size)
        plt.rc("figure", titlesize=size + 4, titleweight="bold")


class GridPlotter(PlotHelperMixin):

    DEFAULT_FONT_SIZE = 8

    def __init__(self, subplotter, results, title, output_dir=None, **plot_opts):
        self._subplotter = subplotter
        self._results = results
        self._title = title
        self._output_dir = output_dir
        self._plot_opts = plot_opts

    def plot(self):
        num_results = len(self._results)
        fig_size = math.ceil(math.sqrt(num_results))

        fig = plt.figure(constrained_layout=True)
        gridspec = fig.add_gridspec(fig_size, fig_size)

        self._set_font_size(self.DEFAULT_FONT_SIZE)

        for i in range(fig_size):
            for j in range(fig_size):
                result_idx = i * fig_size + j
                if result_idx >= num_results:
                    break
                result = self._results[result_idx]

                ax = fig.add_subplot(gridspec[i, j])
                self._subplotter.plot(ax, *result)

        plt.suptitle(self._title)

        plt.savefig(self._get_filename())
        plt.show()

    def _get_filename(self):
        return os.path.join(self._output_dir, "metrics" + "." + "png")


class Plotter(PlotHelperMixin):

    def __init__(self, ymin=None, ymax=None, xmarkers=None, ymarkers=None):
        self._ymin = ymin
        self._ymax = ymax
        self._xmarkers = xmarkers
        self._ymarkers = ymarkers

    @abc.abstractmethod
    def plot(self, fig, title, x, y):
        """Draws plot based on provided data."""


class TimeseriesPlotter(Plotter):

    def plot(self, fig, title, x, y):
        # plot data
        fig.plot(x, y)

        # set title
        fig.set_title(title)

        # set axis labels
        fig.set_xlabel("Time")
        fig.set_ylabel("Value")

        # set limits on y axis
        ymin = self._ymin
        ymin = ymin if ymin and ymin < min(y) else None

        ymax = self._ymax
        ymax = ymax if ymax and ymax > max(y) else None

        fig.set_ylim([ymin, ymax])

        # set time formating on x axis
        time_fmt = mdates.DateFormatter("%H:%M")
        fig.xaxis.set_major_formatter(time_fmt)

        # plot vertical markers
        for xval in self._xmarkers:
            xval_dt = utils.timestamp_to_datetime(xval)
            fig.axvline(x=xval_dt, color="red")

        # plot horizontal markers
        for yval in self._ymarkers:
            fig.axhline(y=yval, color="red")

        fig.grid(True)


class CorrelationMatrixPlotter:

    def __init__(self, corr_matrix):
        self._corr_matrix = corr_matrix

    def plot(self):
        sb.heatmap(
            self._corr_matrix,
            annot=False,
            vmax=1.0, vmin=-1.0,
            cmap='RdYlGn_r',
            linewidths=0.3,
            xticklabels=True,
            yticklabels=True)

        plt.show()

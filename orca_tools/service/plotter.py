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


class MetricGridPlotter(PlotHelperMixin):

    def __init__(self, title, results, output_dir=None, **plot_opts):
        self._title = title
        self._results = results
        self._output_dir = output_dir
        self._plot_opts = plot_opts

    def run(self):
        num_results = len(self._results)
        fig_size = math.floor(math.sqrt(num_results))

        self._set_font_size(8)

        fig = plt.figure(constrained_layout=True)
        gridspec = fig.add_gridspec(fig_size, fig_size)

        for i in range(fig_size):
            for j in range(fig_size):
                result_idx = i * fig_size + j
                if result_idx >= num_results:
                    break
                result = self._results[result_idx]

                ax = fig.add_subplot(gridspec[i, j])
                plotter = TimeseriesPlotter(ax, *result, **self._plot_opts)
                plotter.run()

        plt.suptitle(self._title)

        plt.savefig(self._get_filename())
        plt.show()

    def _get_filename(self):
        return os.path.join(self._output_dir, "metrics" + "." + "png")


class Plotter(PlotHelperMixin):

    def __init__(self, fig, title, x, y, **plot_opts):
        self._fig = fig
        self._title = title
        self._x = x
        self._y = y
        ymin = plot_opts.get("ymin")
        ymax = plot_opts.get("ymax")
        self._ymin = ymin if ymin and ymin < min(y) else None
        self._ymax = ymax if ymax and ymax > max(y) else None
        self._xmarkers = plot_opts.get("xmarkers")
        self._ymarkers = plot_opts.get("ymarkers")

    @abc.abstractmethod
    def run(self):
        """Draws plot based on provided data."""


class TimeseriesPlotter(Plotter):

    def run(self):
        self._fig.plot(self._x, self._y)
        self._fig.set_title(self._title)

        self._fig.set_ylabel("Value")
        self._fig.set_xlabel("Time")
        self._fig.set_ylim([self._ymin, self._ymax])

        time_fmt = mdates.DateFormatter("%H:%M")
        self._fig.xaxis.set_major_formatter(time_fmt)

        for xval in self._xmarkers:
            xval_dt = utils.timestamp_to_datetime(xval)
            self._fig.axvline(x=xval_dt, color="red")

        for yval in self._ymarkers:
            self._fig.axhline(y=yval, color="red")

        self._fig.grid(True)

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

import math
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from orca_tools.common import logger

LOG = logger.get_logger(__name__)


class Plotter:

    def _set_font_size(self, size):
        plt.rc("font", size=size)
        plt.rc("axes", titlesize=size + 2)
        plt.rc("axes", labelsize=size)
        plt.rc("xtick", labelsize=size)
        plt.rc("ytick", labelsize=size)
        plt.rc("legend", fontsize=size)
        plt.rc("figure", titlesize=size + 4, titleweight="bold")


class MetricGridPlotter(Plotter):

    def __init__(self, name, results, output_dir):
        self._name = name
        self._results = results
        self._output_dir = output_dir

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
                plotter = MetricPlotter(ax, *result)
                plotter.run()

        plt.suptitle(self._name)

        plt.savefig(self._get_filename())
        plt.show()

    def _get_filename(self):
        return os.path.join(self._output_dir, "metrics" + "." + "png")


class MetricPlotter(Plotter):

    def __init__(self, fig, name, x, y):
        self._fig = fig
        self._name = name
        self._x = x
        self._y = y

    def run(self):
        self._fig.plot(self._x, self._y)
        self._fig.set_title(self._name)

        self._fig.set_ylabel("Value")
        self._fig.set_xlabel("Time")

        time_fmt = mdates.DateFormatter("%H:%M")
        self._fig.xaxis.set_major_formatter(time_fmt)

        self._fig.grid(True)

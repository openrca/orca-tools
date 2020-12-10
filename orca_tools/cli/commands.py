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
import os
import re

from orca_tools.clients.prometheus import client as prometheus
from orca_tools.common import logger, utils
from orca_tools.service import metrics, plotter

LOG = logger.get_logger(__name__)


class Command(abc.ABC):

    @abc.abstractmethod
    def execute(self, args):
        """Executes command with arguments."""

    def _cast_or_none(self, value, cast_fn):
        if value:
            return cast_fn(value)


class DumpMetrics(Command):

    def execute(self, args):
        title = args["<title>"]
        query = args["<query>"]

        now = utils.get_utc()
        start = int(args["--start"] or now - 500)
        end = int(args["--end"] or now)
        step = int(args["--step"] or 10)

        exp_start = int(args["--exp-start"])
        exp_duration = int(args["--exp-duration"] or 300)
        exp_offset = int(args["--exp-offset"] or 120)

        if exp_start:
            start = exp_start - exp_offset
            end = exp_start + exp_duration + exp_offset

        ymin = self._cast_or_none(args["--ymin"], float)
        ymax = self._cast_or_none(args["--ymax"], float)

        xmarkers = [float(xval) for xval in args["--xmarker"]]
        ymarkers = [float(yval) for yval in args["--ymarker"]]

        output_dir = args.get("--output-dir") or os.getcwd()

        LOG.info(
            "Dumping query '%s', start: %s, end: %s, step: %s",
            query, start, end, step)
        prom_client = prometheus.PrometheusClient.get()
        metric_fetcher = metrics.MetricFetcher(prom_client)
        results = metric_fetcher.run(query, start, end, step)

        LOG.info("Plotting metrics...")
        metric_plotter = plotter.GridPlotter(
            title, results,
            ymin=ymin, ymax=ymax,
            xmarkers=xmarkers, ymarkers=ymarkers,
            output_dir=output_dir)
        metric_plotter.plot()


def get_command(args):
    cmd_class = get_command_class(args)
    return cmd_class()


def get_command_class(args):
    if args["dump-metrics"]:
        return DumpMetrics

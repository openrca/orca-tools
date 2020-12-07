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


class DumpMetrics(Command):

    def execute(self, args):
        query = args['<query>']
        now = utils.get_utc()
        start = int(args['<start>'] or now - 500)
        end = int(args['<end>'] or now)
        step = int(args['<step>'] or 10)
        output_dir = args.get('--output-dir') or os.getcwd()
        LOG.info(
            "Dumping query '%s', start: %s, end: %s, step: %s",
            query, start, end, step)
        prom_client = prometheus.PrometheusClient.get()
        metric_fetcher = metrics.MetricFetcher(prom_client)
        results = metric_fetcher.run(query, start, end, step)
        LOG.info("Plotting metrics...")
        metric_plotter = plotter.MetricGridPlotter(results, output_dir)
        metric_plotter.run()


def get_command(args):
    cmd_class = get_command_class(args)
    return cmd_class()


def get_command_class(args):
    if args['dump-metrics']:
        return DumpMetrics

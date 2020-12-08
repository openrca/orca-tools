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

from datetime import datetime

from orca_tools.clients.prometheus import client as prom_client
from orca_tools.common import logger

LOG = logger.get_logger(__name__)


class MetricFetcher:

    def __init__(self, prom_client):
        self._prom_client = prom_client

    def run(self, query, start, end, step):
        LOG.info("Fetching metric data")
        results = self._prom_client.range_query(query, start, end, step)
        LOG.info("Processing metric data")
        return [self._process_metric(result) for result in results["data"]["result"]]

    def _process_metric(self, result):
        raw_metric = result["metric"]
        raw_values = result["values"]
        name = self._expand_metric_name(raw_metric)
        timestamps, values = self._normalize_values(raw_values)
        return (name, timestamps, values)

    def _expand_metric_name(self, raw_metric):
        keys = sorted(raw_metric.keys())
        values = [raw_metric[key] for key in keys]
        return ".".join(values)

    def _normalize_values(self, raw_values):
        timestamps = []
        values = []
        for raw_value in raw_values:
            timestamp = self._extract_datetime(raw_value[0])
            timestamps.append(timestamp)
            values.append(float(raw_value[1]))
        return timestamps, values

    def _extract_datetime(self, timestamp):
        return datetime.fromtimestamp(int(timestamp))

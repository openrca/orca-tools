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

from orca_tools.clients.prometheus import client as prom_client
from orca_tools.common import logger

LOG = logger.get_logger(__name__)


class MetricFetcher:

    def __init__(self, prom_client):
        self._prom_client = prom_client

    def run(self, metric, namespace, start, end, step):
        query = '%s{namespace="%s"}' % (metric, namespace)
        LOG.info("Fetching metric data")
        results = self._prom_client.range_query(query, start, end, step)
        LOG.info("Processing metric data")
        return [self._process_metric(result) for result in results['data']['result']]

    def _process_metric(self, result):
        raw_metric = result['metric']
        raw_values = result['values']
        name = self._expand_metric_name(raw_metric)
        timestamps, values = self._normalize_values(raw_values)
        return (name, timestamps, values)

    def _expand_metric_name(self, raw_metric):
        namespace = raw_metric.get('namespace', 'unknown-namespace')
        pod_name = raw_metric.get('pod', 'unknown-pod')
        name = raw_metric['__name__']
        return "%s.%s.%s" % (namespace, pod_name, name)

    def _normalize_values(self, raw_values):
        timestamps = []
        values = []
        for raw_value in raw_values:
            timestamps.append(int(raw_value[0]))
            values.append(float(raw_value[1]))
        return timestamps, values

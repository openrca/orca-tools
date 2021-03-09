# Copyright 2021 OpenRCA Authors
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

from orca_tools.clients import rest_client


class OpenRCAClient(rest_client.APIClient):

    """Client for OpenRCA API."""

    def get_alerts(self, time_point=None):
        return self._connector.get("alerts", time_point=time_point)

    def get_graph(self, time_point=None):
        return self._connector.get("graph", time_point=time_point)

    @classmethod
    def get(cls, url="http://localhost:8080", api_prefix="/api/v1"):
        connector = rest_client.APIConnector(url, api_prefix=api_prefix)
        return cls(connector)

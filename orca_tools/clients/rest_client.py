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

import requests
from requests import exceptions as req_exceptions

from orca_tools import exceptions
from orca_tools.clients import utils


class APIClient(object):

    def __init__(self, connector):
        self._connector = connector


class APIConnector(object):

    def __init__(self, url, api_prefix=None, auth=None, timeout=5):
        self._base_url = utils.join_url_paths(url, api_prefix)
        self._auth = auth
        self._timeout = timeout

    def get(self, path, **params):
        url = utils.join_url_paths(self._base_url, path)
        try:
            response = requests.get(url, params=params, auth=self._auth, timeout=self._timeout)
            response.raise_for_status()
            data = response.json()
        except req_exceptions.RequestException as ex:
            raise exceptions.APIClientError(reason=str(ex))
        return data

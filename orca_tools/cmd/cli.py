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

"""OpenRCA Tools
Usage:
    orca-tools dump-metrics
    orca-tools -h | --help
"""

from docopt import docopt

from orca_tools import exceptions
from orca_tools.cli import commands as cmd
from orca_tools.common import logger

LOG = logger.get_logger(__name__)


def main():
    args = docopt(__doc__)
    try:
        cmd.get_command(args).execute(args)
    except exceptions.OrcaToolsError as ex:
        LOG.error("An error ocurred while executing the command: %s", str(ex))

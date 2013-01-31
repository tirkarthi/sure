#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <Sure - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import sys
import optparse

import sure
from sure.runner import Runner

__path__ = os.path.abspath(os.path.dirname(__file__))


def main(args=sys.argv[1:]):
    parser = optparse.OptionParser(
        usage="%prog or type %prog -h (--help) for help",
        version=sure.version)

    parser.add_option("-v", "--verbosity",
                      dest="verbosity",
                      default=3,
                      help='The verbosity level')

    parser.add_option("-s", "--scenarios",
                      dest="scenarios",
                      default=None,
                      help='Comma separated list of scenarios to run')

    parser.add_option("-t", "--tag",
                      dest="tags",
                      default=None,
                      action='append',
                      help='Tells sure to run the specified tags only; '
                      'can be used multiple times to define more tags'
                      '(prefixing tags with "-" will exclude them and '
                      'prefixing with "~" will match approximate words)')

    parser.add_option("--plugin-path",
                      dest="plugin_paths",
                      default=os.path.join(os.getcwdu(), 'sure_plugins'),
                      action='append',
                      help='')

    parser.add_option("-r", "--random",
                      dest="random",
                      action="store_true",
                      default=False,
                      help="Randomize all the tests before running")

    parser.add_option("--stop",
                      dest="failfast",
                      default=False,
                      action="store_true",
                      help='Stop running in the first failure')

    parser.add_option("--pdb",
                      dest="auto_pdb",
                      default=False,
                      action="store_true",
                      help='Launches an interactive debugger upon error')

    parser.add_option("-R", "--reporter",
                      dest="reporter",
                      default='spec',
                      help='Sets what reporter')

    options, args = parser.parse_args(args)
    lookup_paths = list(args)

    base_path = os.getcwdu()

    if not lookup_paths:
        lookup_paths = [
            os.path.join(base_path, 'specs'),
            os.path.join(base_path, 'tests'),
        ]

    tags = None
    if options.tags:
        tags = [tag.strip('@') for tag in options.tags]

    runner = Runner(
        base_path,
        reporter_name=options.reporter,
        random=options.random,
        failfast=options.failfast,
        auto_pdb=options.auto_pdb,
        plugin_paths=options.plugin_paths,
        tags=tags,
    )

    result = runner.run(lookup_paths)
    raise SystemExit(not result.ok)

if __name__ == '__main__':
    main()

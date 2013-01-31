#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2013>  Gabriel Falcão <gabriel@nacaolivre.org>
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
import fnmatch
import importlib

__path__ = os.path.abspath(os.path.abspath(__file__))


def find_recursive(base_path, glob='*'):
    ret = []
    if base_path == __path__:
        return ret

    for root, dirs, files in os.walk(base_path, topdown=False):
        if not root.startswith(base_path) or root.startswith(__path__):
            break

        paths = map(lambda name: os.path.join(root, name), files)
        ret.extend(fnmatch.filter(paths, glob))

    return ret


def load_recursive(base_path, ignore_errors=True):
    mods = []
    for fullpath in find_recursive(base_path, '*.py'):
        path, filename = os.path.split(fullpath)
        name = os.path.splitext(filename)[0]
        sys.path.append(path)
        try:
            mods.append(importlib.import_module(name))
        except ImportError:
            if not ignore_errors:
                raise

        finally:
            sys.path.remove(path)

    return mods

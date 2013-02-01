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
import re
import sys
import inspect
import traceback

from sure import importer
from sure.reporter import Reporter


def stripped(string):
    return "\n".join(filter(bool, [s.strip() for s in string.splitlines()]))


class TestResult(object):
    def __init__(self, results):
        self.results = results

    def __nonzero__(self):
        return self.ok

    @property
    def ok(self):
        return all([x.ok for x in self.results])


class TestCaseResult(TestResult):
    def __init__(self, case, error=None):
        self.case = case
        self.error = error

    def printable(self):
        if self.is_error:
            return self.error.printable()
        elif self.is_failure:
            return "\n".join(traceback.format_exception(*self.error))
        else:
            return ""

    @property
    def is_error(self):
        return isinstance(self.error, ErrorStack)

    @property
    def is_failure(self):
        return isinstance(self.error, tuple)

    @property
    def is_success(self):
        return self.error is None

    @property
    def ok(self):
        return self.is_success


class TestSuiteResult(TestResult):
    pass


class FinalTestSuiteResult(TestResult):
    pass


class TestSuite(object):
    def __init__(self, module):
        name = getattr(module, 'suite_name', module.__name__)
        description = getattr(module, 'suite_description', "")

        self.name = stripped(name)
        self.description = stripped(description)

        self.module = module
        self.ready = False
        self.testcases = []

    def load_cases(self, executables):
        self.testcases = map((lambda e: TestCase(e, self)), executables)
        self.ready = True
        return self.testcases

    def run(self, reporter):
        results = []
        for case in self.testcases:
            reporter.on_test(case)
            result = case.run(reporter)
            results.append(result)

            if result.is_error:
                reporter.on_error(case, result)

            elif result.is_failure:
                reporter.on_failure(case, result)

            else:
                reporter.on_success(case)

            reporter.on_test_done(case, result)

        return TestSuiteResult(results)


class ErrorStack(object):
    def __init__(self, exception_info):
        self.exception_info = exception_info
        self.traceback = traceback.format_exception(*exception_info)

    def printable(self):
        return "\n".join(self.traceback)


class TestCase(object):
    def __init__(self, class_or_callable, suite):
        fallback = class_or_callable.__name__

        self.description = stripped(class_or_callable.__doc__ or fallback)

        self.object = class_or_callable
        self.suite = suite

    def run(self, reporter):
        try:
            self.object()
        except AssertionError:
            return TestCaseResult(self, sys.exc_info())
        except:
            return TestCaseResult(self, ErrorStack(sys.exc_info()))
        else:
            return TestCaseResult(self)


class Runner(object):
    u"""Manages I/O operations to find tests and execute them"""

    def __init__(self, base_path, reporter_name, plugin_paths=None, **kwargs):
        self.base_path = base_path
        self.plugin_paths = plugin_paths or []

        self.reporter = Reporter.from_name_and_runner(reporter_name, self)

        for k in kwargs:
            setattr(self, k, kwargs.get(k))

    def __repr__(self):
        return u'<Runner: {}>'.format(self.base_path)

    def find_candidates(self, lookup_paths):
        candidate_modules = []
        for path in map(os.path.abspath, lookup_paths):
            candidate_modules.extend(importer.load_recursive(path))

        return candidate_modules

    def is_runnable_test(self, item):
        try:
            name = item.__name__
        except AttributeError:
            return
        else:

            return re.search(r'(^Test|^Spec|Spec$|Test$)', name, re.I)

    def extract_members(self, candidate):
        all_members = [m[1] for m in inspect.getmembers(candidate)]
        members = filter(self.is_runnable_test, all_members)
        return candidate, members

    def load_suites(self, lookup_paths):
        suites = []
        cases = []
        candidates = self.find_candidates(lookup_paths)
        for module, executables in map(self.extract_members, candidates):
            suite = TestSuite(module)
            cases.extend(suite.load_cases(executables))
            suites.append(suite)

        return suites

    def run(self, lookup_paths):
        results = []
        self.reporter.on_start()

        for suite in self.load_suites(lookup_paths):
            self.reporter.on_suite(suite)
            result = suite.run(self.reporter)
            results.append(result)
            self.reporter.on_suite_done(suite, result)

        self.reporter.on_finish()

        return FinalTestSuiteResult(results)

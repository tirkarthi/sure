#!/usr/bin/env python
# -*- coding: utf-8 -*-


def ensuring_the_runner_constructor(spec):
    "The Runner class constructor"
    from sure.runner import Runner

    spec.Runner = Runner


def ensure_it_takes_base_path(spec):
    "takes base_path and reporter name"
    # Given get_reporter returns a fake value
    spec.Runner.get_reporter = spec.mock.get_reporter
    spec.Runner.get_reporter.return_value = "should be a reporter"

    # When the runner is instantiated
    runner = spec.Runner("/some-path", "some-reporter")

    # Then it should have the given base_path
    runner.base_path.should.equal("/some-path")

    # And it should have the expected reporter
    runner.reporter.should.equal("some-reporter")

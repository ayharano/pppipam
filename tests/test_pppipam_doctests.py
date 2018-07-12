#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for description methods of pppipam.AddressSpace instances."""

import doctest
import unittest

from pppipam import helpers, pppipam


def load_tests(loader, tests, ignore):
    """Base example provided in doctest documentation."""
    tests.addTests(doctest.DocTestSuite(helpers))
    tests.addTests(doctest.DocTestSuite(pppipam))
    return tests

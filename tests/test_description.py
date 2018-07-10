#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for description methods of pppipam.AddressSpace instances."""

import unittest
from pppipam.pppipam import AddressSpace


class AddressSpace_description_TestCase(unittest.TestCase):
    """Tests for description related methods."""

    def setUp(self):
        """Set up test fixtures with new AddressSpace."""
        self.address_space = AddressSpace()

    def test_address_space_as_AddressSpace(self):
        """Validate if address_space is instance of AddressSpace."""
        self.assertIsInstance(self.address_space, AddressSpace)

    def test_describe_keyword_only_no_empty_arguments(self):
        """describe method as keyword only, without default parameters."""
        no_empty_arguments = False
        try:
            self.address_space.describe()
        except TypeError:
            no_empty_arguments = True
        self.assertTrue(
            no_empty_arguments,
            "Empty arguments should not be accepted in describe",
        )

    def test_describe_address(self):
        """Add valid IP address with non-empty str description."""
        self.assertIs(
            self.address_space.describe('123.123.123.123', "123 is nice"),
            True,
        )
